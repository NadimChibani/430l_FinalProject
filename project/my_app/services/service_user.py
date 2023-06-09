from flask import jsonify
from project.my_app.models.user import User, user_schema
from project.my_app.services.service_validator import service_validator

class ServiceUser:
    def __init__(self, storage_instance):
        self.storage = storage_instance

    def get_user(self,user_id):
        service_validator.validate_user_id(user_id)
        return self.storage.get_user(user_id)

    def add_new_user(self,user_name,password):
        service_validator.validate_user_input(user_name,password)
        service_validator.validate_user_input_already_exists(user_name)
        new_User = User(user_name,password)
        self.storage.add_to_database(new_User)
        return jsonify(user_schema.dump(new_User))
    
    def authenticate_user(self,user_name,password):
        service_validator.validate_user_input(user_name,password)
        existsInDatabase = service_validator.validate_user_exists(user_name,password)
        return jsonify({"token":create_token(existsInDatabase.id),"role":existsInDatabase.user_type})
    
from project.my_app.app import create_token, storage
service_user = ServiceUser(storage)