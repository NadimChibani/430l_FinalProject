from flask import Blueprint
from ..app import jsonify
from project.my_app.services.service_statistics import calculate_averages_given_information, get_all_transactions_last_three_days

blueprint_statistics = Blueprint(name="blueprint_statistics", import_name=__name__)

@blueprint_statistics.route('/exchangeRate' ,methods=['GET'])
def handle_rate_check():
    usd_to_lbp_Transactions = get_all_transactions_last_three_days(True)
    lbp_to_usd_Transactions = get_all_transactions_last_three_days(False)
    usd_to_lbp, lbp_to_usd = calculate_averages_given_information(usd_to_lbp_Transactions,lbp_to_usd_Transactions)

    return jsonify(
        usd_to_lbp = usd_to_lbp,
        lbp_to_usd = lbp_to_usd
    )