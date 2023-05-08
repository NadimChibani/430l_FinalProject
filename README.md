To run this project:

1- create a virtual environment
2- run pip install requirements.text
3- venv/Scripts/activate
4- flask run

This backend was done by Nadim Chibani
Link to swagger documentation: https://app.swaggerhub.com/apis-docs/NadimChibani/Alpha-Exchange-Rate/2.1

The software architecture/design pattern used is the model view controller used to isolate between three layers:
The controller layer which deals wich receives the http requests
The service layer which deals with all the business logic
The storage layer which deals with interactions with the database

The storage key used for the database is deployed on heroku as a secret