from project.my_app.models.transaction import Transaction

def get_all_transactions_of_user(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return transactions

def get_all_transactions_ordered_by_date_and_type(usd_to_lbp):
    transactions = Transaction.query.filter(Transaction.usd_to_lbp == usd_to_lbp).order_by(Transaction.added_date.desc()).all()
    return transactions
