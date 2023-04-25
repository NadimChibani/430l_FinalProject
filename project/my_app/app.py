from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
import jwt
import datetime
from flask import Response
import json
#from project.my_app import db_config

app = Flask(__name__)

bcrypt = Bcrypt(app)
ma = Marshmallow(app)

#Had to put it here wasn't working otherwise need to test now that comfirmed working
DB_CONFIG = 'mysql://b1f4047b288625:32f778fa@eu-cdbr-west-03.cleardb.net/heroku_831116c766fd72a'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
db = SQLAlchemy(app)

from project.my_app.model.user import User, user_schema
from project.my_app.model.transaction import Transaction, transaction_schema, transactions_schema #, transactions_data_schema, transactions_date_schema

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None
    
def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']

#Python
# >>> from app import app,db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()

@app.route('/user',methods=['POST'])
def handle_new_user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    validateUserInput(user_name,password)

    validateUserInputAlreadyExists(user_name)
    new_User = User(user_name,password)
    addToDatabase(new_User)

    return jsonify(user_schema.dump(new_User))

@app.route('/authentication',methods=['POST'])
def handle_user_authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    validateUserInput(user_name,password)

    existsInDatabase = validateUserExists(user_name,password)
    return jsonify({"token":create_token(existsInDatabase.id)})

@app.route('/transaction',methods=['POST'])
def handle_insert():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]
    validateTransactionInput(usd_amount,lbp_amount,usd_to_lbp)
    authentication_token = extract_auth_token(request)
    user_id = validateAuthenticationToken(authentication_token)

    new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp,user_id)
    addToDatabase(new_Transaction)
    return jsonify(transaction_schema.dump(new_Transaction)),201

@app.route('/transaction',methods=['GET'])
def handle_extract():
    authentication_token = extract_auth_token(request)
    checkAuthenticationTokenNotNull(authentication_token)
    user_id = validateAuthenticationToken(authentication_token)
    transactions = getAllTransactionsOfUser(user_id)
    return jsonify(transactions_schema.dump(transactions))

@app.route('/exchangeRate' ,methods=['GET'])
def handle_Rate_Check():
    usd_to_lbp_Transactions = getAllTransactionsLastThreeDays(True)
    lbp_to_usd_Transactions = getAllTransactionsLastThreeDays(False)
    usd_to_lbp_Total = sumAllRates(usd_to_lbp_Transactions)
    lbp_to_usd_Total = sumAllRates(lbp_to_usd_Transactions)
    usd_to_lbp = getRateAverage(usd_to_lbp_Total,len(usd_to_lbp_Transactions))
    lbp_to_usd = getRateAverage(lbp_to_usd_Total,len(lbp_to_usd_Transactions))

    return jsonify(
        usd_to_lbp = usd_to_lbp,
        lbp_to_usd = lbp_to_usd
    )

def getAllTransactionsLastThreeDays(usd_to_lbp):
    return Transaction.query.filter(Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3),datetime.datetime.now()),Transaction.usd_to_lbp == usd_to_lbp).all()

def sumAllRates(list):
    sum = 0
    for i in list:
        sum += i.lbp_amount/i.usd_amount
    return sum

def getRateAverage(total,listlength):
    if(listlength==0):
        return "NO DATA"
    return total/listlength

def validateTransactionInput(usd_amount,lbp_amount,usd_to_lbp):
    if(usd_amount==None or lbp_amount==None or usd_to_lbp==None or usd_amount=="" or lbp_amount=="" or usd_to_lbp==""):
        abort(400, 'UsdAmount or LbpAmount or TransactionType cannot be empty')
    if(usd_amount<0):
        abort(400, 'UsdAmount cannot be negative')
    if(lbp_amount<0):
        abort(400, 'LbpAmount cannot be negative')
    if(usd_amount==0):
        abort(400, 'UsdAmount cannot be zero')
    if(lbp_amount==0):
        abort(400, 'LbpAmount cannot be zero')

def validateUserInput(user_name,password):
    if(user_name==None or user_name=="" or password==None or password==""):
        abort(400, 'Username or Password cannot be empty')

def validateUserInputAlreadyExists(user_name):
    if(User.query.filter_by(user_name=user_name).first()):
        abort(409, 'User '+ user_name+' already exists')

def validateUserExists(user_name,password):
    existsInDatabase = User.query.filter_by(user_name=user_name).first()
    if(existsInDatabase == None):
        abort(404, 'User '+ user_name+' does not exist')
    if not bcrypt.check_password_hash(existsInDatabase.hashed_password, password):
        abort(403, 'Incorrect password')
    return existsInDatabase

def validateAuthenticationToken(authentication_token):
    if(authentication_token == None):
        return None
    try:
        user_id = decode_token(authentication_token)
        if(user_id==None or user_id==0 or not User.query.filter_by(id=user_id).first()):
            abort(403, 'Authentication token not linked to existing user')
        return user_id
    except:
        abort(403, 'Invalid authentication token')

def addToDatabase(object):
    try:
        db.session.add(object)
        db.session.commit()
    except:
        abort(500, 'Error adding to database')

def checkAuthenticationTokenNotNull(authentication_token):
    if(authentication_token == None):
        abort(403, 'Authentication token not provided')

def getAllTransactionsOfUser(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return transactions

def getAllTransactionOrderedByDateAndType(usd_to_lbp):
    transactions = Transaction.query.filter(Transaction.usd_to_lbp == usd_to_lbp).order_by(Transaction.added_date.desc()).all()
    return transactions

@app.route('/transaction/datapoints' ,methods=['GET'])
#for now going to do the send all data points, later will do the averages if needed
def get_hourly_transaction_averages():
    #first have to determine the start and end dates
    usd_transactions = getAllTransactionOrderedByDateAndType(usd_to_lbp = True)
    usd_transactionsDataList = transactions_schema.dump(usd_transactions)

    lbp_transactions = getAllTransactionOrderedByDateAndType(usd_to_lbp = False)
    lbp_transactionsDataList = transactions_schema.dump(lbp_transactions)

    return Response(json.dumps({'usd data points' : usd_transactionsDataList,
                                'lbp data point' : lbp_transactionsDataList,}),  mimetype='application/json')

    # start_date_str = request.args.get('start_date', default='1 hour ago', type=str)
    # end_date_str = request.args.get('end_date', default='now', type=str)
    # try:
    #     start_date = datetime.fromisoformat(start_date_str)
    # except ValueError:
    #     start_date = datetime.utcnow() - timedelta(hours=1)
    # try:
    #     end_date = datetime.fromisoformat(end_date_str)
    # except ValueError:
    #     end_date = datetime.utcnow()

    # delta = timedelta(hours=1)
    # current_date = start_date
    # hourly_averages = []
    # while current_date <= end_date:
    #     next_date = current_date + delta
    #     query = db.session.query(db.func.avg(Transaction.amount)).filter(Transaction.created_at >= current_date, Transaction.created_at < next_date)
    #     hourly_average = query.scalar()
    #     if hourly_average:
    #         hourly_averages.append(hourly_average)
    #     current_date = next_date
    
    # response_data = {'averages': hourly_averages}


    # return jsonify(response_data)

with app.app_context():
    db.create_all()