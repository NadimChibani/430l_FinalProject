from flask import abort
from project.my_app.app import db
from project.my_app.models.user import User

class Storage:
    def __init__(self, db):
        self.db = db

    def add_to_database(self,object):
        try:
            self.db.session.add(object)
            db.session.commit()
        except:
            abort(500, 'Error adding to database')

def get_user(user_id):
    return User.query.filter_by(id=user_id).first()