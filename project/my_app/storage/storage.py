import datetime
from flask import abort
from project.my_app.app import db
from project.my_app.models.news import News
from project.my_app.models.transaction import Transaction
from project.my_app.models.user import User
from project.my_app.models.usertransaction import UserTransaction

class Storage:
    def __init__(self, db):
        self.db = db

    def add_to_database(self,object):
        try:
            self.db.session.add(object)
            db.session.commit()
        except:
            abort(500, 'Error adding to database')

    def get_all_transactions_of_user(self,user_id):
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return transactions

    def get_all_transactions_ordered_by_date_and_type(self,usd_to_lbp):
        transactions = Transaction.query.filter(Transaction.usd_to_lbp == usd_to_lbp).order_by(Transaction.added_date.desc()).all()
        return transactions

    def get_all_transactions_last_three_days(self,usd_to_lbp):
        return Transaction.query.filter(
            Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3),datetime.datetime.now())
            ,Transaction.usd_to_lbp == usd_to_lbp
            ).all()
            
    def get_all_username_usertransactions(self,seller_username):
        transaction_where_seller =  UserTransaction.query.filter_by(seller_username=seller_username).all()
        transaction_where_buyer =  UserTransaction.query.filter_by(buyer_username=seller_username).all()
        return transaction_where_seller + transaction_where_buyer

    def get_all_offers_usertransactions(self):
        return UserTransaction.query.filter_by(status="available").all()

    def get_specific_usertransaction(self,usertransaction_id):
        result = UserTransaction.query.filter_by(id=usertransaction_id).first()
        if(result == None):
            abort(404, 'UserTransaction not found')
        return result
    
    def handle_number_of_news(self):
        news = News.query.order_by(News.added_date.desc()).all()
        if len(news) == 3:
            News.query.filter_by(id=news[2].id).delete()

    def get_all_news(self):
        return News.query.order_by(News.added_date.desc()).all()

    def get_user(self,user_id):
        return User.query.filter_by(id=user_id).first()
    

