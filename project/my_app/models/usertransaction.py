from ..app import db, ma, datetime

class UserTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_username = db.Column(db.String(30), db.ForeignKey('user.user_name'),nullable=False)
    buyer_username = db.Column(db.String(30), db.ForeignKey('user.user_name'),nullable=True)

    usd_amount = db.Column(db.Float,nullable=False)
    lbp_amount = db.Column(db.Float,nullable=False)
    usd_to_lbp = db.Column(db.Boolean,nullable=False)
    added_date = db.Column(db.DateTime)
    status = db.Column(db.String(45),nullable=False)
    seller_phone_number = db.Column(db.String(45),nullable=True)

    seller_confirmation = db.Column(db.Boolean,nullable=True)
    buyer_confirmation = db.Column(db.Boolean,nullable=True)


    def __init__(self, seller_username, usd_amount, lbp_amount, usd_to_lbp,seller_phone_number):
        super(UserTransaction, self).__init__(
            seller_username=seller_username,
            buyer_username=None,
            usd_amount=usd_amount,  
            lbp_amount=lbp_amount, 
            usd_to_lbp=usd_to_lbp,
            added_date=datetime.datetime.now(),
            status = "available",
            seller_confirmation = False,
            buyer_confirmation = False,
            seller_phone_number = seller_phone_number
        )


class UserTransactionSchema(ma.Schema):
    class Meta:
        fields = ("id","seller_username","buyer_username", "usd_amount", "lbp_amount", "usd_to_lbp","added_date", "status","seller_phone_number")
        model = UserTransaction

class UserTransactionConfirmationSchema(ma.Schema):
    class Meta:
        fields = ("id","seller_username","buyer_username", "usd_amount", "lbp_amount", "usd_to_lbp","added_date", "status","seller_confirmation","buyer_confirmation","seller_phone_number")
        model = UserTransaction

usertransaction_schema = UserTransactionSchema()
usertransactions_schema = UserTransactionSchema(many=True)
usertransaction_confirmation_schema = UserTransactionConfirmationSchema()