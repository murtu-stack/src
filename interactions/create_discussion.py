from models.user import User
from models.discussion import Discussion

def create_discussion(user_name, discussion_data):
    user = User.select().where(User.user_name == user_name).first()
    if user:
        return Discussion.create(user=user, **discussion_data)
    return None