from project.my_app.app import datetime
from project.my_app.models.transaction import Transaction
from project.my_app.services.service_statistics import calculate_averages_given_information

def get_all_transactions_of_user(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return transactions

def get_all_transactions_ordered_by_date_and_type(usd_to_lbp):
    transactions = Transaction.query.filter(Transaction.usd_to_lbp == usd_to_lbp).order_by(Transaction.added_date.desc()).all()
    return transactions

def get_all_transactions_last_three_days(usd_to_lbp):
    return Transaction.query.filter(
        Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3),datetime.datetime.now())
        ,Transaction.usd_to_lbp == usd_to_lbp
        ).all()

def get_all_transactions_between_two_dates(current_date,next_step_date,usd_transactions,lbp_transactions):
    filtered_usd_transactions = [t for t in usd_transactions if next_step_date <= t.added_date <= current_date]
    filtered_lbp_transactions = [t for t in lbp_transactions if next_step_date <= t.added_date <= current_date]
    return filtered_usd_transactions,filtered_lbp_transactions

def get_all_averages_based_on_timeStep(usd_transactions,lbp_transactions,timeStep,start_date,end_date):
    # current_date = datetime.datetime.utcnow() # because of the location where the server or database is hosted
    # start_date = datetime.datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S %Z")
    # end_date = datetime.datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S %Z")
    start_date = datetime.datetime.fromtimestamp(start_date)
    end_date = datetime.datetime.fromtimestamp(end_date) - timeStep
    # return start_date,end_date,end_date
    current_date = start_date
    next_step_date = current_date - timeStep
    # return start_date,end_date,next_step_date
    averagesUsd = []
    averagesLbp = []
    dates = []
    while end_date<next_step_date:
        filtered_usd_transactions, filtered_lbp_transactions = get_all_transactions_between_two_dates(current_date,next_step_date,usd_transactions,lbp_transactions)
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
