from flask import jsonify
from project.my_app.app import datetime, extract_auth_token, get_id_from_authentication, validate_authentication_token
from project.my_app.models.transaction import Transaction, transaction_schema, transactions_schema
from project.my_app.services.service_statistics import calculate_averages_given_information
from project.my_app.services.validator_transaction import validate_dates, validate_transaction_input
import joblib
import os
from project.my_app.services.validator_transaction import validate_future_date


class ServiceTransaction:
    def __init__(self, storage_instance):
        self.storage = storage_instance
        dirname = os.path.dirname(__file__)
        self.loaded_model_lbp = joblib.load(os.path.join(dirname, 'model_lbp.sav'))
        self.loaded_model_usd = joblib.load(os.path.join(dirname, 'model_usd.sav'))


    def add_transaction(self,usd_amount,lbp_amount,usd_to_lbp,request):
        validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp)
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
        validate_dates(start_date,end_date)
        if(timeFormat == "Hourly"):
            timeStep =  datetime.timedelta(hours=1)
        elif(timeFormat == "Daily"):
            timeStep =  datetime.timedelta(days=1)
        elif(timeFormat == "Weekly"):
            timeStep =  datetime.timedelta(weeks=1)

        averagesUsd, averagesLbp, dates = self.get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date)
        response_data = {'averagesUsdToLbp': averagesUsd,
                        'averagesLbpToUsd': averagesLbp,
                        'dates': dates,}
        return jsonify(response_data)
    
    def predict(self,date):
        validate_future_date(date)
        result_lbp = self.loaded_model_lbp.predict([[date]])
        result_usd = self.loaded_model_usd.predict([[date]])
        return jsonify({"lbp_to_usd_rate": result_lbp[0],
                        "usd_to_lbp_rate": result_usd[1]
                        })

    def get_all_transactions_between_two_dates(self,current_date,next_step_date,usd_transactions,lbp_transactions):
        filtered_usd_transactions = [t for t in usd_transactions if next_step_date <= t.added_date <= current_date]
        filtered_lbp_transactions = [t for t in lbp_transactions if next_step_date <= t.added_date <= current_date]
        return filtered_usd_transactions,filtered_lbp_transactions

    def get_all_averages_based_on_timeStep(self,usd_transactions,lbp_transactions,timeStep,start_date,end_date):
        start_date = datetime.datetime.fromtimestamp(start_date)
        end_date = datetime.datetime.fromtimestamp(end_date) - timeStep
        current_date = start_date
        next_step_date = current_date - timeStep
        averagesUsd = []
        averagesLbp = []
        dates = []
        while end_date<next_step_date:
            filtered_usd_transactions, filtered_lbp_transactions = self.get_all_transactions_between_two_dates(current_date,next_step_date,usd_transactions,lbp_transactions)
            usd_average,lbp_average = calculate_averages_given_information(filtered_usd_transactions,filtered_lbp_transactions)
            if(usd_average == "NO DATA"):
                usd_average = -1.0
            if(lbp_average == "NO DATA"):
                lbp_average = -1.0
            averagesUsd.append(float(usd_average))
            averagesLbp.append(float(lbp_average))
            dates.append(current_date)
            current_date = next_step_date
            next_step_date = next_step_date - timeStep
        return averagesUsd,averagesLbp,dates

from project.my_app.app import storage
service_transaction = ServiceTransaction(storage)