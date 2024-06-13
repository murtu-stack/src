from interactions.get_user import get_user
from models.comment import Comment

def create_comment(user_id, comment_data):
    user = get_user(user_id)
    if user:
        return Comment.create(user=user, **comment_data)
    return None