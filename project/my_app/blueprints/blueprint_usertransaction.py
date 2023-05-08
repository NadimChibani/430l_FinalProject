from flask import Blueprint

from project.my_app.services.service_usertransaction import confirm_buyer_seller, get_all_offers_usertransactions, get_all_username_usertransactions, get_specific_usertransaction
from project.my_app.services.validator_user import validate_seller_not_buyer, validate_user_phone_number
from ..app import db, get_id_from_authentication, request, datetime, relativedelta, add_to_database, jsonify, create_token, extract_auth_token, check_authentication_token_not_null, validate_authentication_token
from project.my_app.services.validator_transaction import validate_transaction_input
from project.my_app.models.usertransaction import UserTransaction, usertransaction_schema, usertransactions_schema, usertransaction_confirmation_schema
from project.my_app.services.service_user import get_user

blueprint_usertransaction = Blueprint(name="blueprint_usertransaction", import_name=__name__)

@blueprint_usertransaction.route('/usertransaction',methods=['POST'])
def handle_insert():
    usd_amount = request.json["usd_amount"]
    lbp_amount = request.json["lbp_amount"]
    usd_to_lbp = request.json["usd_to_lbp"]
    seller_phone_number = request.json["seller_phone_number"]
    validate_transaction_input(usd_amount,lbp_amount,usd_to_lbp)
    validate_user_phone_number(seller_phone_number)
    authentication_token = extract_auth_token(request)
    user_id = validate_authentication_token(authentication_token)
    seller_username = get_user(user_id).user_name
    new_UserTransaction = UserTransaction(
        seller_username = seller_username,
        usd_amount=usd_amount,
        lbp_amount=lbp_amount,
        usd_to_lbp=usd_to_lbp,
        seller_phone_number=seller_phone_number,
    )
    add_to_database(new_UserTransaction)
    return jsonify(usertransaction_schema.dump(new_UserTransaction)),201

#TODO add validation for seller is buyer, and that the transaction is pending
@blueprint_usertransaction.route('/usertransaction/list/user',methods=['GET'])
def handle_get_all():
    # authentication_token = extract_auth_token(request)
    # user_id = validate_authentication_token(authentication_token)
    user_id = get_id_from_authentication(request)
    seller_username = get_user(user_id).user_name
    usertransactions = get_all_username_usertransactions(seller_username)
    return jsonify(usertransactions_schema.dump(usertransactions)),200

@blueprint_usertransaction.route('/usertransaction/list/offers',methods=['GET'])
def handle_get_all_offers():
    usertransactions = get_all_offers_usertransactions()
    return jsonify(usertransactions_schema.dump(usertransactions)),200

@blueprint_usertransaction.route('/usertransaction/reserve',methods=['PUT'])
def handle_reserve():
    usertransaction_id = request.json["usertransaction_id"]
    # authentication_token = extract_auth_token(request)
    # user_id = validate_authentication_token(authentication_token)
    user_id = get_id_from_authentication(request)
    buyer_username = get_user(user_id).user_name
    usertransaction = get_specific_usertransaction(usertransaction_id)
    validate_seller_not_buyer(usertransaction,buyer_username)
    usertransaction.buyer_username = buyer_username
    usertransaction.status = "reserved"
    db.session.commit()
    return jsonify(usertransaction_schema.dump(usertransaction)),200

@blueprint_usertransaction.route('/usertransaction/confirm',methods=['PUT'])
def handle_confirm():
    usertransaction_id = request.json["usertransaction_id"]
    # authentication_token = extract_auth_token(request)
    # user_id = validate_authentication_token(authentication_token)
    user_id = get_id_from_authentication(request)
    usertransaction = get_specific_usertransaction(usertransaction_id)
    usertransaction = confirm_buyer_seller(usertransaction,user_id)
    db.session.commit()
    response_data = {'userTransactionUpdated': usertransaction_confirmation_schema.dump(usertransaction)}
    return jsonify(response_data),200