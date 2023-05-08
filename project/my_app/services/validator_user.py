from flask import abort
from project.my_app.models.user import User
from project.my_app.app import bcrypt, decode_token
import re

def validate_user_input(user_name,password):
    regex_pattern_username = r'^[^\d\W][\w$#@%!?&]{0,30}$'
    regex_pattern_password = r'^[^\d\W][\w$#@%!?&+-]*$'
    if not re.match(regex_pattern_username, str(user_name)) or not re.match(regex_pattern_password, str(password)):
        abort(400, 'Username or Password is incorrect')
    if(user_name==None or user_name=="" or password==None or password==""):
        abort(400, 'Username or Password is incorrect')

def validate_user_input_already_exists(user_name):
    if(User.query.filter_by(user_name=user_name).first()):
        abort(409, 'User '+ user_name+' already exists')

def validate_user_exists(user_name,password):
    existsInDatabase = User.query.filter_by(user_name=user_name).first()
    if(existsInDatabase == None):
        abort(404, 'User '+ user_name+' does not exist')
    if not bcrypt.check_password_hash(existsInDatabase.hashed_password, password):
        abort(403, 'Username or Password is incorrect')
    return existsInDatabase

def validate_user_id(user_id):
    if user_id == None or user_id == "":
        abort(400, 'User not found')

def validate_user_not_in_transaction(username):
    abort(403, 'User '+ username+' is not part of transaction')

from project.my_app.services.service_user import get_user

def validate_user_role(role, user_id):
    user = get_user(user_id)
    if user.user_type != role:
        abort(403, 'Privilege not allowed')
    return user

def validate_user_phone_number(phone_number):
    regex_pattern = r'^\d{8}$'
    if not re.match(regex_pattern, str(phone_number)):
        abort(400, 'Phone number is incorrect')
    if phone_number==None or phone_number=="":
        abort(400, 'Phone number is incorrect')

def validate_seller_not_buyer(usertransaction,buyer_username):
    if usertransaction.seller_username == buyer_username:
        abort(403, 'Seller cannot reserve his own offer')