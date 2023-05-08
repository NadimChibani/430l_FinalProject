import datetime
# from sklearn import datasets, linear_model
# from sklearn import linear_model
# from sklearn.linear_model import LinearRegression
# from project.my_app.services.service_transaction import get_all_averages_based_on_timeStep, get_all_transactions_ordered_by_date_and_type
# import pandas as pd
# from dateutil.relativedelta import relativedelta
import joblib
import os

dirname = os.path.dirname(__file__)

loaded_model_lbp = joblib.load(os.path.join(dirname, 'model_lbp.sav'))
loaded_model_usd = joblib.load(os.path.join(dirname, 'model_usd.sav'))

def predict(date):
    result_lbp = loaded_model_lbp.predict([[date]])
    result_usd = loaded_model_usd.predict([[date]])
    return result_lbp[0],result_usd[0]




