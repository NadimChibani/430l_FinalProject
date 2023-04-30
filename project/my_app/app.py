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
import os
import sys
from dateutil.relativedelta import relativedelta
from project.my_app.db_config import DB_CONFIG

app = Flask(__name__)

bcrypt = Bcrypt(app)
ma = Marshmallow(app)

# DB_CONFIG = os.environ["DB_CONFIG"]

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
db = SQLAlchemy(app)

def add_to_database(object):
    try:
        db.session.add(object)
        db.session.commit()
    except:
        abort(500, 'Error adding to database')

from project.my_app.models.user import User
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

def validate_authentication_token(authentication_token):
    if(authentication_token == None):
        return None
    try:
        user_id = decode_token(authentication_token)
        if(user_id==None or user_id==0 or not User.query.filter_by(id=user_id).first()):
            abort(403, 'Authentication token not linked to existing user')
        return user_id
    except:
        abort(403, 'Invalid authentication token')

#Python
# >>> from app import app,db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()

def check_authentication_token_not_null(authentication_token):
    if(authentication_token == None):
        abort(403, 'Authentication token not provided')

from project.my_app.blueprints.blueprint_user import blueprint_user
from project.my_app.blueprints.blueprint_statistics import blueprint_statistics
from project.my_app.blueprints.blueprint_transaction import blueprint_transaction
app.register_blueprint(blueprint_user, url_prefix="")
app.register_blueprint(blueprint_statistics, url_prefix="")
app.register_blueprint(blueprint_transaction, url_prefix="")

with app.app_context():
    db.create_all()
