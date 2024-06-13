from models.user import User

def get_user(user_id):
    return User.get_or_none(User.id == user_id)