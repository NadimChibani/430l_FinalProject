from flask import Blueprint#, request, jsonify
from ..app import request, add_to_database, jsonify, create_token
from project.my_app.models.user import User, user_schema
from project.my_app.services.validator_user import validate_user_input, validate_user_input_already_exists, validate_user_exists

blueprint_user = Blueprint(name="blueprint_user", import_name=__name__)

@blueprint_user.route('/user',methods=['POST'])
def handle_new_user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    validate_user_input(user_name,password)

    validate_user_input_already_exists(user_name)
    new_User = User(user_name,password)
    add_to_database(new_User)

    return jsonify(user_schema.dump(new_User))

@blueprint_user.route('/authentication',methods=['POST'])
def handle_user_authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    validate_user_input(user_name,password)

    existsInDatabase = validate_user_exists(user_name,password)
    return jsonify({"token":create_token(existsInDatabase.id),"role":existsInDatabase.user_type})
