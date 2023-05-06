from flask import abort
from project.my_app.models.user import User
from project.my_app.app import bcrypt, decode_token
from project.my_app.services.service_user import get_user

def validate_user_input(user_name,password):
    if(user_name==None or user_name=="" or password==None or password==""):
        abort(400, 'Username or Password cannot be empty')

def validate_user_input_already_exists(user_name):
    if(User.query.filter_by(user_name=user_name).first()):
        abort(409, 'User '+ user_name+' already exists')

def validate_user_exists(user_name,password):
    existsInDatabase = User.query.filter_by(user_name=user_name).first()
    if(existsInDatabase == None):
        abort(404, 'User '+ user_name+' does not exist')
    if not bcrypt.check_password_hash(existsInDatabase.hashed_password, password):
        abort(403, 'Incorrect username or incorrect password')
    return existsInDatabase

def validate_user_id(user_id):
    if user_id == None or user_id == "":
        abort(400, 'User id not found')

def validate_user_not_in_transaction(username):
    abort(403, 'User '+ username+' is not part of transaction')

def validate_user_role(role, user_id):
    user = get_user(user_id)
    if user.user_type != role:
        abort(403, 'Privilege not allowed')
    return user