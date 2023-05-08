from flask import Blueprint
from ..app import get_id_from_authentication, request,datetime,relativedelta, add_to_database, jsonify, create_token, extract_auth_token, check_authentication_token_not_null, validate_authentication_token
from project.my_app.models.transaction import Transaction, transaction_schema, transactions_schema
from project.my_app.services.validator_transaction import validate_transaction_input
from project.my_app.services.service_transaction import get_all_averages_based_on_timeStep, get_all_transactions_of_user, get_all_transactions_ordered_by_date_and_type, get_all_transactions_between_two_dates

blueprint_transaction = Blueprint(name="blueprint_transaction", import_name=__name__)

@blueprint_transaction.route('/transaction',methods=['POST'])
def handle_insert():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]
    validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp)
    # authentication_token = extract_auth_token(request)
    # user_id = validate_authentication_token(authentication_token)
    user_id = get_id_from_authentication(request)

    new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp,user_id)
    add_to_database(new_Transaction)
    return jsonify(transaction_schema.dump(new_Transaction)),201

@blueprint_transaction.route('/transaction',methods=['GET'])
def handle_extract():
    user_id = get_id_from_authentication(request)
    transactions = get_all_transactions_of_user(user_id)
    return jsonify(transactions_schema.dump(transactions))


@blueprint_transaction.route('/transaction/datapoints' ,methods=['POST'])
def get_time_based_transaction_averages():
    usd_transactions = get_all_transactions_ordered_by_date_and_type(usd_to_lbp = True)
    lbp_transactions = get_all_transactions_ordered_by_date_and_type(usd_to_lbp = False)

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

    averagesUsd, averagesLbp, dates = get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date)
    response_data = {'averagesUsdToLbp': averagesUsd,
                     'averagesLbpToUsd': averagesLbp,
                     'dates': dates,}
    return jsonify(response_data)