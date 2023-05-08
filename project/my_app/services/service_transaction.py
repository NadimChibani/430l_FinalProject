from flask import jsonify
from project.my_app.app import datetime, extract_auth_token, get_id_from_authentication, validate_authentication_token
from project.my_app.models.transaction import Transaction, transaction_schema, transactions_schema
from project.my_app.services.service_statistics import get_all_averages_based_on_timeStep
from project.my_app.services.service_validator import service_validator


class ServiceTransaction:
    def __init__(self, storage_instance):
        self.storage = storage_instance

    def add_transaction(self,usd_amount,lbp_amount,usd_to_lbp,request):
        service_validator.validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp)
        authentication_token = extract_auth_token(request)
        if(authentication_token == None):
            user_id = None
        else:
            user_id = validate_authentication_token(authentication_token)
        new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp,user_id)
        self.storage.add_to_database(new_Transaction)
        return jsonify(transaction_schema.dump(new_Transaction)),201

    def get_all_user_transactions(self,request):
        user_id = get_id_from_authentication(request)
        transactions = self.storage.get_all_transactions_of_user(user_id)
        return jsonify(transactions_schema.dump(transactions))
    
    def get_time_based_transaction_averages(self,timeFormat,start_date,end_date):
        usd_transactions = self.storage.get_all_transactions_ordered_by_date_and_type(usd_to_lbp = True)
        lbp_transactions = self.storage.get_all_transactions_ordered_by_date_and_type(usd_to_lbp = False)
        service_validator.validate_dates(start_date,end_date)
        if(timeFormat == "Hourly"):
            timeStep =  datetime.timedelta(hours=1)
        elif(timeFormat == "Daily"):
            timeStep =  datetime.timedelta(days=1)
        elif(timeFormat == "Weekly"):
            timeStep =  datetime.timedelta(weeks=1)

        averagesUsd, averagesLbp, dates = get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date)
        response_data = {'averagesUsdToLbp': averagesUsd,
                        'averagesLbpToUsd': averagesLbp,
                        'dates': dates,}
        return jsonify(response_data)
    
    def get_all_transactions_between_two_dates(self,current_date,next_step_date,usd_transactions,lbp_transactions):
        filtered_usd_transactions = [t for t in usd_transactions if next_step_date <= t.added_date <= current_date]
        filtered_lbp_transactions = [t for t in lbp_transactions if next_step_date <= t.added_date <= current_date]
        return filtered_usd_transactions,filtered_lbp_transactions

from project.my_app.app import storage
service_transaction = ServiceTransaction(storage)