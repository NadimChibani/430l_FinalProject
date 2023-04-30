from project.my_app.app import datetime
from project.my_app.models.transaction import Transaction

def calculate_averages_given_information(usd_to_lbp_Transactions,lbp_to_usd_Transactions):
    usd_to_lbp_Total = sum_all_rates(usd_to_lbp_Transactions)
    lbp_to_usd_Total = sum_all_rates(lbp_to_usd_Transactions)
    usd_to_lbp = get_rate_average(usd_to_lbp_Total,len(usd_to_lbp_Transactions))
    lbp_to_usd = get_rate_average(lbp_to_usd_Total,len(lbp_to_usd_Transactions))
    return usd_to_lbp,lbp_to_usd

def get_all_transactions_last_three_days(usd_to_lbp):
    return Transaction.query.filter(
        Transaction.added_date.between(datetime.datetime.now() - datetime.timedelta(days=3),datetime.datetime.now())
        ,Transaction.usd_to_lbp == usd_to_lbp
        ).all()

def sum_all_rates(list):
    sum = 0
    for i in list:
        sum += i.lbp_amount/i.usd_amount
    return sum

def get_rate_average(total,listlength):
    if(listlength==0):
        return "NO DATA"
    return total/listlength