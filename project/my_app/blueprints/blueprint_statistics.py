from flask import Blueprint
from ..app import request

class ControllerStatistics:
    def __init__(self, service_statistics):
        self.service_statistics = service_statistics

    def handle_rate_check(self):
        return self.service_statistics.get_exchange_rate()
    
    def handle_statistics(self):
        timeFormat = request.json['timeFormat']
        start_date = request.json['startDate']
        end_date = request.json['endDate']
        return self.service_statistics.get_statistics(timeFormat,start_date,end_date)

    def predict_rate(self):
        date = request.json["date"]
        return self.service_statistics.predict(date)

from project.my_app.services.service_statistics import service_statistics
controller_statistics = ControllerStatistics(service_statistics)

blueprint_statistics = Blueprint(name="blueprint_statistics", import_name=__name__)

@blueprint_statistics.route('/exchangeRate' ,methods=['GET'])
def handle_rate_check():
    return controller_statistics.handle_rate_check()

@blueprint_statistics.route('/statistics' ,methods=['POST'])
def handle_statistics():
    return controller_statistics.handle_statistics()

@blueprint_statistics.route('/datapoints/predict' ,methods=['POST'])
def predict_rate():
    return controller_statistics.predict_rate()
