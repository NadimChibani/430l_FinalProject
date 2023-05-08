from flask import abort, jsonify
from project.my_app.app import extract_auth_token, get_id_from_authentication, validate_authentication_token
from project.my_app.models.transaction import Transaction
from project.my_app.models.usertransaction import UserTransaction, usertransaction_schema, usertransactions_schema, usertransaction_confirmation_schema
from project.my_app.storage.storage import get_user
from project.my_app.services.validator_transaction import validate_transaction_input, validate_usertransaction
from project.my_app.services.validator_user import validate_seller_not_buyer, validate_user_not_in_transaction, validate_user_phone_number

class ServiceTransaction:
    def __init__(self, storage_instance):
        self.storage = storage_instance
    
    def add_usertransaction(self,usd_amount,lbp_amount,usd_to_lbp,seller_phone_number,request):
        validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp)
        validate_user_phone_number(seller_phone_number)
        authentication_token = extract_auth_token(request)
        user_id = validate_authentication_token(authentication_token)
        seller_username = get_user(user_id).user_name
        new_UserTransaction = UserTransaction(
            seller_username = seller_username,
            usd_amount=usd_amount,
            lbp_amount=lbp_amount,
            usd_to_lbp=usd_to_lbp,
            seller_phone_number=seller_phone_number,
        )
        self.storage.add_to_database(new_UserTransaction)
        return jsonify(usertransaction_schema.dump(new_UserTransaction)),201

    def get_all_usertransactions(self,request):
        user_id = get_id_from_authentication(request)
        seller_username = get_user(user_id).user_name
        usertransactions = self.storage.get_all_username_usertransactions(seller_username)
        return jsonify(usertransactions_schema.dump(usertransactions)),200

    def get_all_offers_usertransactions(self):
        usertransactions = self.storage.get_all_offers_usertransactions()
        return jsonify(usertransactions_schema.dump(usertransactions)),200

    def reserve_usertransaction(self,usertransaction_id,request):
        validate_usertransaction(usertransaction_id)
        user_id = get_id_from_authentication(request)
        buyer_username = get_user(user_id).user_name
        usertransaction = self.storage.get_specific_usertransaction(usertransaction_id)
        validate_seller_not_buyer(usertransaction,buyer_username)
        usertransaction.buyer_username = buyer_username
        usertransaction.status = "reserved"
        self.storage.db.session.commit()
        return jsonify(usertransaction_schema.dump(usertransaction)),200

    def confirm_usertransaction(self,usertransaction_id,request):
        validate_usertransaction(usertransaction_id)
        user_id = get_id_from_authentication(request)
        usertransaction = self.storage.get_specific_usertransaction(usertransaction_id)
        usertransaction = self.storage.confirm_buyer_seller(usertransaction,user_id)
        self.storage.db.session.commit()
        response_data = {'userTransactionUpdated': usertransaction_confirmation_schema.dump(usertransaction)}
        return jsonify(response_data),200

    def confirm_buyer_seller(self,usertransaction,user_id):
        username = get_user(user_id).user_name
        if usertransaction.buyer_username == username:
            usertransaction.buyer_confirmation = True
        elif usertransaction.seller_username == username:
            usertransaction.seller_confirmation = True
        else:
            validate_user_not_in_transaction(username)
        if usertransaction.buyer_confirmation and usertransaction.seller_confirmation:
            usertransaction.status = "confirmed"
            self.add_usertransaction_to_transaction(usertransaction,user_id)
        return usertransaction

    def add_usertransaction_to_transaction(self,usertransaction,user_id):
        transaction = Transaction(usertransaction.usd_amount, usertransaction.lbp_amount, usertransaction.usd_to_lbp,user_id)
        self.storage.add_to_database(transaction)
