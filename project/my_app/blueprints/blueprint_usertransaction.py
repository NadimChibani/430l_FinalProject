from flask import Blueprint
from ..app import  request

class ControllerUserTransaction:
    def __init__(self, service_usertransaction):
        self.service_usertransaction = service_usertransaction

    def handle_insert(self):
        usd_amount = request.json["usd_amount"]
        lbp_amount = request.json["lbp_amount"]
        usd_to_lbp = request.json["usd_to_lbp"]
        seller_phone_number = request.json["seller_phone_number"]
        return self.service_usertransaction.add_usertransaction(usd_amount,lbp_amount,usd_to_lbp,seller_phone_number,request)

    def handle_get_all(self):
        return self.service_usertransaction.get_all_usertransactions(request)

    def handle_get_all_offers(self):
        return self.service_usertransaction.get_all_offers_usertransactions()
    
    def handle_reserve(self):
        usertransaction_id = request.json["usertransaction_id"]
        return self.service_usertransaction.reserve_usertransaction(usertransaction_id,request)
    
    def handle_confirm(self):
        usertransaction_id = request.json["usertransaction_id"]
        return self.service_usertransaction.confirm_usertransaction(usertransaction_id,request)

from project.my_app.services.service_usertransaction import service_usertransaction
controller_usertransaction = ControllerUserTransaction(service_usertransaction)

blueprint_usertransaction = Blueprint(name="blueprint_usertransaction", import_name=__name__)

@blueprint_usertransaction.route('/usertransaction',methods=['POST'])
def handle_insert():
    return controller_usertransaction.handle_insert()

@blueprint_usertransaction.route('/usertransaction/list/user',methods=['GET'])
def handle_get_all():
    return controller_usertransaction.handle_get_all()

@blueprint_usertransaction.route('/usertransaction/list/offers',methods=['GET'])
def handle_get_all_offers():
    return controller_usertransaction.handle_get_all_offers()

@blueprint_usertransaction.route('/usertransaction/reserve',methods=['PUT'])
def handle_reserve():
    return controller_usertransaction.handle_reserve()

@blueprint_usertransaction.route('/usertransaction/confirm',methods=['PUT'])
def handle_confirm():
    return controller_usertransaction.handle_confirm()