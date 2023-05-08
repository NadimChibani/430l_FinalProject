from flask import Blueprint
from ..app import request

class ControllerTransaction:
    def __init__(self, service_transaction):
        self.service_transaction = service_transaction

    def handle_insert(self):
        usd_amount = request.json["usd_amount"]
        lbp_amount = request.json["lbp_amount"]
        usd_to_lbp = request.json["usd_to_lbp"]
        return self.service_transaction.add_transaction(usd_amount,lbp_amount,usd_to_lbp,request)

    def handle_extract(self):
        return self.service_transaction.get_all_user_transactions(request)

    def get_time_based_transaction_averages(self):
        timeFormat = request.json['timeFormat']
        start_date = request.json['startDate']
        end_date = request.json['endDate']
        return self.service_transaction.get_time_based_transaction_averages(timeFormat,start_date,end_date)

from project.my_app.services.service_transaction import service_transaction
controller_transaction = ControllerTransaction(service_transaction)

blueprint_transaction = Blueprint(name="blueprint_transaction", import_name=__name__)

@blueprint_transaction.route('/transaction',methods=['POST'])
def handle_insert():
    return controller_transaction.handle_insert()

@blueprint_transaction.route('/transaction',methods=['GET'])
def handle_extract():
    return controller_transaction.handle_extract()

@blueprint_transaction.route('/transaction/datapoints' ,methods=['POST'])
def get_time_based_transaction_averages():
    return controller_transaction.get_time_based_transaction_averages()
