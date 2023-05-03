from project.my_app.models.user import User
from project.my_app.services.validator_user import validate_user_id

def get_user(user_id):
    validate_user_id(user_id)
    return User.query.filter_by(id=user_id).first()