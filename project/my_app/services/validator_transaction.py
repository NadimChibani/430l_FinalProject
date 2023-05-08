import datetime
from flask import abort
import re

def validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp):
    regex_pattern = r'^\d{1,10}$'
    if not re.match(regex_pattern, str(usd_amount)) or not re.match(regex_pattern, str(lbp_amount)):
        abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')
    if usd_amount ==0 or lbp_amount ==0:
        abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')
    if not isinstance(usd_to_lbp, bool) or usd_to_lbp == None or usd_to_lbp == "":
        abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')

def validate_usertransaction(transaction_id):
    if transaction_id == None or transaction_id == "" or transaction_id <= 0 or transaction_id>2147483647:
        abort(400, 'Transaction is incorrect')

def validate_dates(start_date,end_date):
    if start_date == None or start_date == "" or end_date == None or end_date == "":
        abort(400, 'Dates are incorrect')
    if start_date < end_date:
        abort(400, 'Dates are incorrect')
    if start_date<1672531200 or end_date<1672531200:
        abort(400, 'Dates are too old incorrect')

def validate_future_date(date):
    if date < datetime.datetime.now().timestamp():
        abort(400, 'Date is incorrect')

    
    