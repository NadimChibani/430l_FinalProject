from flask import abort

def validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp):
    if(usd_amount==None or lbp_amount==None or usd_to_lbp==None or usd_amount=="" or lbp_amount=="" or usd_to_lbp=="" or usd_amount<0 or lbp_amount<0 or usd_amount==0 or lbp_amount==0):
        abort(400, 'UsdAmount or LbpAmount or TransactionType is incorrect')

