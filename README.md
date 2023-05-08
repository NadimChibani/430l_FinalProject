To run this project:

1- create a virtual environment
2- run pip install requirements.text
3- venv/Scripts/activate
4- flask run

This backend was done by Nadim Chibani
Link to swagger documentation: https://app.swaggerhub.com/apis-docs/NadimChibani/Alpha-Exchange-Rate/2.2
Repositry link: https://github.com/NadimChibani/430l_FinalProject

The software architecture/design pattern used is the model view controller used to isolate between three layers:
The controller layer which deals wich receives the http requests
The service layer which deals with all the business logic
The storage layer which deals with interactions with the database

The storage key used for the database is deployed on heroku as a secret

References used:

- chatgpt

Regular expression generation:
- https://www.websense.com/content/support/library/email/hosted/admin_guide/regex.aspx
- https://regex101.com/r/YiRKnV/1
- https://laasyasettyblog.hashnode.dev/validating-username-using-regex
- https://www.ibm.com/docs/en/app-connect/11.0.0?topic=elements-message-sets-regular-expression-syntax

For unix timestamp:
- https://www.epochconverter.com/

For naming conventions:
- https://peps.python.org/pep-0008/#class-names

For flask and flask project layout:
- https://flask.palletsprojects.com/en/2.2.x/api/
- https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/
- https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2019/flask-api-project-layout/
