from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
import jwt
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ndragon5@localhost:3306/exchange'
CORS(app)
db = SQLAlchemy(app)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float,nullable=False)
    lbp_amount = db.Column(db.Float,nullable=False)
    usd_to_lbp = db.Column(db.Boolean,nullable=False)
    added_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
    nullable=True)

    def __init__(self, usd_amount, lbp_amount,usd_to_lbp):
        self.usd_amount = usd_amount
        self.lbp_amount = lbp_amount
        self.usd_to_lbp = usd_to_lbp

    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id):
        super(Transaction, self).__init__(usd_amount=usd_amount,
        lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp,
        user_id=user_id,
        added_date=datetime.datetime.now())


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "usd_amount", "lbp_amount", "usd_to_lbp","added_date","user_id")
        model = Transaction


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    def __init__(self, user_name, password):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
        model = User
user_schema = UserSchema()

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

    new_User = User(user_name,password)

    db.session.add(new_User)
    db.session.commit()

    return jsonify(user_schema.dump(new_User))

@app.route('/authentication',methods=['POST'])
def handle_user_authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    
    if(user_name==None or user_name=="" or password==None or password==""):
        abort(400)
    
    existsInDatabase = User.query.filter_by(user_name=user_name).first()
    
    if(existsInDatabase == None):
        abort(403)

    if not bcrypt.check_password_hash(existsInDatabase.hashed_password, password):
        abort(403)

    return jsonify({"token":create_token(existsInDatabase.id)})

@app.route('/transaction',methods=['POST'])
def handle_insert():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]
    authentication_token = extract_auth_token(request)
    
    if (authentication_token != None):
        user_id = decode_token(authentication_token)
        
        if(user_id==None or user_id==0 or not User.query.filter_by(id=user_id).first()):
            abort(403)

        new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp,user_id)
    else:
        new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp,None)

    db.session.add(new_Transaction)
    db.session.commit()

    return jsonify(transaction_schema.dump(new_Transaction))

@app.route('/transaction',methods=['GET'])
def handle_extract():
    authentication_token = extract_auth_token(request)
    if (authentication_token != None):
        user_id = decode_token(authentication_token)
        if(not User.query.filter_by(id=user_id).first()):
            abort(403)
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return jsonify(transactions_schema.dump(transactions))


@app.route('/exchangeRate' ,methods=['GET'])
def handle_Rate_Check():
    usd_to_lbp_Transactions = Transaction.query.filter_by(usd_to_lbp=1).all()
    lbp_to_usd_Transactions = Transaction.query.filter_by(usd_to_lbp=0).all()

    usd_to_lbp_Total = 0
    lbp_to_usd_Total = 0

    for i in usd_to_lbp_Transactions:
        usd_to_lbp_Total += i.usd_amount/i.lbp_amount 

    for i in lbp_to_usd_Transactions:
        lbp_to_usd_Total += i.lbp_amount/i.usd_amount 

    #if no data for each case
    if(len(usd_to_lbp_Transactions)!=0):
        usd_to_lbp = usd_to_lbp_Total/len(usd_to_lbp_Transactions)
    else:
        lbp_to_usd = "NO DATA"   

    if(len(lbp_to_usd_Transactions)!=0):
        lbp_to_usd = lbp_to_usd_Total/len(lbp_to_usd_Transactions)
    else:
        lbp_to_usd = "NO DATA"

    return jsonify(
        usd_to_lbp = usd_to_lbp,
        lbp_to_usd = lbp_to_usd
    )

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

with app.app_context():
    db.create_all()