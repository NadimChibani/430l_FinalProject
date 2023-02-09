from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ndragon5@localhost:3306/exchange'
db = SQLAlchemy(app)

#with app.app_context:
#   db.create_all()


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usd_amount = db.Column(db.Float,nullable=False)
    lbp_amount = db.Column(db.Float,nullable=False)
    usd_to_lbp = db.Column(db.Boolean,nullable=False)
    def __init__(self, usd_amount, lbp_amount,usd_to_lbp):
        self.usd_amount = usd_amount
        self.lbp_amount = lbp_amount
        self.usd_to_lbp = usd_to_lbp


#Python
# >>> from app import app,db
# >>> app.app_context().push()
# >>> db.create_all()
# >>> exit()


@app.route('/transaction',methods=['POST'])
def handle_insert():
    usd_amount = request.json["usd_amount"]
    print(usd_amount)
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]
    
    new_Transaction = Transaction(usd_amount,lbp_amount,usd_to_lbp)

    db.session.add(new_Transaction)
    db.session.commit()

    return jsonify(
            message="Success",
            category="success",
            status=200
      )
