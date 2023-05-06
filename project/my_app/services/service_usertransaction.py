from project.my_app.app import add_to_database
from project.my_app.models.transaction import Transaction
from project.my_app.models.usertransaction import UserTransaction
from project.my_app.services.service_user import get_user
from project.my_app.services.validator_user import validate_user_not_in_transaction

def get_all_username_usertransactions(seller_username):
    transaction_where_seller =  UserTransaction.query.filter_by(seller_username=seller_username).all()
    transaction_where_buyer =  UserTransaction.query.filter_by(buyer_username=seller_username).all()
    return transaction_where_seller + transaction_where_buyer

def get_all_offers_usertransactions():
    return UserTransaction.query.filter_by(status="available").all()

def get_specific_usertransaction(usertransaction_id):
    return UserTransaction.query.filter_by(id=usertransaction_id).first()

def confirm_buyer_seller(usertransaction,user_id):
    username = get_user(user_id).user_name
    if usertransaction.buyer_username == username:
        usertransaction.buyer_confirmation = True
    elif usertransaction.seller_username == username:
        usertransaction.seller_confirmation = True
    else:
        validate_user_not_in_transaction(username)
    if usertransaction.buyer_confirmation and usertransaction.seller_confirmation:
        usertransaction.status = "confirmed"
        add_usertransaction_to_transaction(usertransaction,user_id)
    return usertransaction

def add_usertransaction_to_transaction(usertransaction,user_id):
    transaction = Transaction(usertransaction.usd_amount, usertransaction.lbp_amount, usertransaction.usd_to_lbp,user_id)
    add_to_database(transaction)
