from flask import Blueprint#, request, jsonify
from ..app import request, jsonify, create_token
from project.my_app.models.user import User, user_schema
from project.my_app.services.validator_user import validate_user_input, validate_user_input_already_exists, validate_user_exists

class ControllerUser:
    def __init__(self, service_user):
        self.service_user = service_user

    def handle_new_user(self):
        user_name = request.json["user_name"]
        password = request.json["password"]
        return self.service_user.add_new_user(user_name,password)

    def handle_user_authentication(self):
        user_name = request.json["user_name"]
        password = request.json["password"]
        return self.service_user.authenticate_user(user_name,password)       
    
from project.my_app.services.service_user import service_user
controller_user = ControllerUser(service_user)

blueprint_user = Blueprint(name="blueprint_user", import_name=__name__)

@blueprint_user.route('/user',methods=['POST'])
def handle_new_user():
    return controller_user.handle_new_user()

@blueprint_user.route('/authentication',methods=['POST'])
def handle_user_authentication():
    return controller_user.handle_user_authentication()
