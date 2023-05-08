# import joblib
# import os

# from project.my_app.services.validator_transaction import validate_future_date

# dirname = os.path.dirname(__file__)

# loaded_model_lbp = joblib.load(os.path.join(dirname, 'model_lbp.sav'))
# loaded_model_usd = joblib.load(os.path.join(dirname, 'model_usd.sav'))

# def predict(date):
#     validate_future_date(date)
#     result_lbp = loaded_model_lbp.predict([[date]])
#     result_usd = loaded_model_usd.predict([[date]])
#     return result_lbp[0],result_usd[0]
