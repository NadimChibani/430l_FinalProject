from flask import abort
from project.my_app.models.user import User
from project.my_app.app import bcrypt, decode_token
import re
import datetime

class ServiceValidator:
    def __init__(self, storage_instance):
        self.storage = storage_instance

    def validate_user_input(self,user_name,password):
        regex_pattern_username = r'^[^\d\W][\w$#@%!?&]{0,30}$'
        regex_pattern_password = r'^[^\d\W][\w$#@%!?&+-]*$'
        if not re.match(regex_pattern_username, str(user_name)) or not re.match(regex_pattern_password, str(password)):
            abort(400, 'Username or Password is incorrect')
        if(user_name==None or user_name=="" or password==None or password==""):
            abort(400, 'Username or Password is incorrect')

    def validate_user_input_already_exists(self,user_name):
        if(User.query.filter_by(user_name=user_name).first()):
            abort(409, 'User '+ user_name+' already exists')

    def validate_user_exists(self,user_name,password):
        existsInDatabase = User.query.filter_by(user_name=user_name).first()
        if(existsInDatabase == None):
            abort(404, 'User '+ user_name+' does not exist')
        if not bcrypt.check_password_hash(existsInDatabase.hashed_password, password):
            abort(403, 'Username or Password is incorrect')
        return existsInDatabase

    def validate_user_id(self,user_id):
        if user_id == None or user_id == "":
            abort(400, 'User not found')

    def validate_user_not_in_transaction(self,username):
        abort(403, 'User '+ username+' is not part of transaction')

    def validate_user_role(self,role, user_id):
        user = self.storage.get_user(user_id)
        if user.user_type != role:
            abort(403, 'Privilege not allowed')
        return user

    def validate_user_phone_number(self,phone_number):
        regex_pattern = r'^\d{8}$'
        if not re.match(regex_pattern, str(phone_number)):
            abort(400, 'Phone number is incorrect')
        if phone_number==None or phone_number=="":
            abort(400, 'Phone number is incorrect')

    def validate_seller_not_buyer(self,usertransaction,buyer_username):
        if usertransaction.seller_username == buyer_username:
            abort(403, 'Seller cannot reserve his own offer')

    def validate_news(self,news):
        regex_pattern = r'^(?=[a-zA-Z])(?=.{1,300}$)(?!.*[<>;"\/\[\]{}()=+&%*#@!,\\]).*$'
        if not re.match(regex_pattern, str(news)):
            abort(400, 'News input is incorrect, please change it')

    def validate_transaction_input(self,usd_amount,lbp_amount,usd_to_lbp):
        # regex_pattern = r'^\d{1,10}$'
        # if not re.match(regex_pattern, str(usd_amount)) or not re.match(regex_pattern, str(lbp_amount)):
        #     abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')
        if usd_amount ==0 or lbp_amount ==0:
            abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')
        if not isinstance(usd_to_lbp, bool) or usd_to_lbp == None or usd_to_lbp == "":
            abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')

    def validate_usertransaction(self,transaction_id):
        if transaction_id == None or transaction_id == "" or transaction_id <= 0 or transaction_id>2147483647:
            abort(400, 'Transaction is incorrect')

    def validate_dates(self,start_date,end_date):
        if start_date == None or start_date == "" or end_date == None or end_date == "":
            abort(400, 'Dates are incorrect')
        if start_date < end_date:
            abort(400, 'Dates are incorrect')
        if start_date<1672531200 or end_date<1672531200:
            abort(400, 'Dates are too old incorrect')

    def validate_future_date(self,date):
        if date < datetime.datetime.now().timestamp():
            abort(400, 'Date is incorrect')

from project.my_app.app import storage
service_validator = ServiceValidator(storage)