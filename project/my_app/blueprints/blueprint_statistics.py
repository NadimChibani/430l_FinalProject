from flask import Blueprint

from project.my_app.services.service_ml import predict
from ..app import jsonify,relativedelta
import datetime
from project.my_app.services.service_statistics import calculate_averages_given_information
from project.my_app.services.service_transaction import get_all_averages_based_on_timeStep, get_all_transactions_last_three_days, get_all_transactions_between_two_dates, get_all_transactions_ordered_by_date_and_type
# from project.my_app.services.service_ml import filename
# import joblib
from ..app import request

blueprint_statistics = Blueprint(name="blueprint_statistics", import_name=__name__)

@blueprint_statistics.route('/exchangeRate' ,methods=['GET'])
def handle_rate_check():
    usd_to_lbp_Transactions = get_all_transactions_last_three_days(True)
    lbp_to_usd_Transactions = get_all_transactions_last_three_days(False)
    usd_to_lbp, lbp_to_usd = calculate_averages_given_information(usd_to_lbp_Transactions,lbp_to_usd_Transactions)

    return jsonify(
        usd_to_lbp = usd_to_lbp,
        lbp_to_usd = lbp_to_usd
    )

@blueprint_statistics.route('/statistics' ,methods=['POST'])
def handle_statistics():
    timeFormat = request.json['timeFormat']
    start_date = request.json['startDate']
    end_date = request.json['endDate']

    if(timeFormat == "Hourly"):
        timeStep =  datetime.timedelta(hours=1)
    #     end_date = datetime.datetime.now() - relativedelta(days = 1)
    elif(timeFormat == "Daily"):
        timeStep =  datetime.timedelta(days=1)
    #     end_date = datetime.datetime.now() - relativedelta(days = 7)
    elif(timeFormat == "Weekly"):
        timeStep =  datetime.timedelta(weeks=1)
    #     end_date = datetime.datetime.now() - relativedelta(months=1)

    # calculating the number of transactions in the last week
    usd_transactions = get_all_transactions_ordered_by_date_and_type(usd_to_lbp = True)
    lbp_transactions = get_all_transactions_ordered_by_date_and_type(usd_to_lbp = False)
    current_date =  datetime.datetime.fromtimestamp(start_date)
    formated_end_date = datetime.datetime.fromtimestamp(end_date)

    next_step_date = current_date - timeStep
    usd_transactions_between_dates, lbp_transactions_between_dates = get_all_transactions_between_two_dates(current_date,formated_end_date,usd_transactions,lbp_transactions)
    nb_usd_transactions_between_dates = len(usd_transactions_between_dates)
    nb_lbp_transactions_between_dates= len(lbp_transactions_between_dates)

    # calculating how much rate changed in the range given
    usd_averages,lbp_averages,dates = get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date)
    usd_rate_drop_between_dates= usd_averages[0] - usd_averages[-1]
    lbp_rate_drop_between_dates = lbp_averages[0] - lbp_averages[-1]

    # calculating the number of transactions today
    timeStep =  datetime.timedelta(days=1)
    next_step_date = current_date - timeStep

    #TODO fix timezone problem
    usd_transactions_today,lbp_transactions_today = get_all_transactions_between_two_dates(current_date,next_step_date,usd_transactions,lbp_transactions)
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

@blueprint_statistics.route('/datapoints/predict' ,methods=['POST'])
def predict_rate():
    date = request.json["date"]
    result = predict(date)
    return jsonify({"lbp_to_usd_rate": result[0],
                    "usd_to_lbp_rate": result[1]
                    })
