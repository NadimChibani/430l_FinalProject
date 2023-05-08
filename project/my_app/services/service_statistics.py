
import datetime
from flask import jsonify

from project.my_app.services.validator_transaction import validate_dates


class ServiceStatistics:
    def __init__(self, storage_instance):
        self.storage = storage_instance

    def get_exchange_rate(self):
        usd_to_lbp_Transactions = self.storage.get_all_transactions_last_three_days(True)
        lbp_to_usd_Transactions = self.storage.get_all_transactions_last_three_days(False)
        usd_to_lbp, lbp_to_usd = calculate_averages_given_information(usd_to_lbp_Transactions,lbp_to_usd_Transactions)

        return jsonify(
            usd_to_lbp = usd_to_lbp,
            lbp_to_usd = lbp_to_usd
        )
    
    def get_statistics(self,timeFormat,start_date,end_date):
        validate_dates(start_date,end_date)
        if(timeFormat == "Hourly"):
            timeStep =  datetime.timedelta(hours=1)
        elif(timeFormat == "Daily"):
            timeStep =  datetime.timedelta(days=1)
        elif(timeFormat == "Weekly"):
            timeStep =  datetime.timedelta(weeks=1)

        current_date =  datetime.datetime.fromtimestamp(start_date)
        formated_end_date = datetime.datetime.fromtimestamp(end_date)

        # calculating the number of transactions in the last week
        usd_transactions = self.storage.get_all_transactions_ordered_by_date_and_type(usd_to_lbp = True)
        lbp_transactions = self.storage.get_all_transactions_ordered_by_date_and_type(usd_to_lbp = False)

        next_step_date = current_date - timeStep
        usd_transactions_between_dates, lbp_transactions_between_dates = self.storage.get_all_transactions_between_two_dates(current_date,formated_end_date,usd_transactions,lbp_transactions)
        nb_usd_transactions_between_dates = len(usd_transactions_between_dates)
        nb_lbp_transactions_between_dates= len(lbp_transactions_between_dates)

        # calculating how much rate changed in the range given
        usd_averages,lbp_averages,dates = self.storage.get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date)
        usd_rate_drop_between_dates= usd_averages[0] - usd_averages[-1]
        lbp_rate_drop_between_dates = lbp_averages[0] - lbp_averages[-1]

        # calculating the number of transactions today
        timeStep =  datetime.timedelta(days=1)
        next_step_date = current_date - timeStep

        #TODO fix timezone problem
        usd_transactions_today,lbp_transactions_today = self.storage.get_all_transactions_between_two_dates(current_date,next_step_date,usd_transactions,lbp_transactions)
        total_transactions_today = len(usd_transactions_today) + len(lbp_transactions_today)
        response_data = {
            'numberOfTransactionsBetweenDates': nb_usd_transactions_between_dates + nb_lbp_transactions_between_dates,
            'numberOfUsdTransactionsBetweenDates': nb_usd_transactions_between_dates,
            'numberOfLbpTransactionsBetweenDates': nb_lbp_transactions_between_dates,
            'usdRateChangeBasedOnTimeFormatBetweenDates': usd_rate_drop_between_dates,
            'lbpRateChangeBasedOnTimeFormatBetweenDates': lbp_rate_drop_between_dates,
            'totalTransactionsToday': total_transactions_today,
            }
        return jsonify(response_data)

def calculate_averages_given_information(usd_to_lbp_Transactions,lbp_to_usd_Transactions):
    usd_to_lbp_Total = sum_all_rates(usd_to_lbp_Transactions)
    lbp_to_usd_Total = sum_all_rates(lbp_to_usd_Transactions)
    usd_to_lbp = get_rate_average(usd_to_lbp_Total,len(usd_to_lbp_Transactions))
    lbp_to_usd = get_rate_average(lbp_to_usd_Total,len(lbp_to_usd_Transactions))
    return usd_to_lbp,lbp_to_usd

def sum_all_rates(list):
    sum = 0
    for i in list:
        sum += i.lbp_amount/i.usd_amount
    return sum

def get_rate_average(total,listlength):
    if(listlength==0):
        return "NO DATA"
    return total/listlength

from project.my_app.app import storage
service_statistics = ServiceStatistics(storage)