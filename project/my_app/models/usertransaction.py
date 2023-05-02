from ..app import db, ma, datetime

class UserTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_username = db.Column(db.String, db.ForeignKey('user.user_name'),nullable=False)
    buyer_username = db.Column(db.String, db.ForeignKey('user.user_name'),nullable=True)

    usd_amount = db.Column(db.Float,nullable=False)
    lbp_amount = db.Column(db.Float,nullable=False)
    usd_to_lbp = db.Column(db.Boolean,nullable=False)
    added_date = db.Column(db.DateTime)
    status = db.Column(db.String(45),nullable=False)


    def __init__(self, usd_amount, lbp_amount, usd_to_lbp, user_id):
        super(UserTransaction, self).__init__(usd_amount=usd_amount,
        lbp_amount=lbp_amount, usd_to_lbp=usd_to_lbp,
        seller_id=user_id,
        added_date=datetime.datetime.now()),
        status = "available"


class UserTransactionSchema(ma.Schema):
    class Meta:
        fields = ("id","seller_id","buyer_id", "usd_amount", "lbp_amount", "usd_to_lbp","added_date", "status")
        model = UserTransaction

user_transaction_schema = UserTransactionSchema()
user_transactions_schema = UserTransactionSchema(many=True)