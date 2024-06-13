from interactions.get_user import get_user  
from interactions.get_comment import get_comment
from models.comment_like import CommentLike

def like_comment(user_id, comment_id):
    user = get_user(user_id)
    comment = get_comment(comment_id)
    if user and comment:
        return CommentLike.create(user=user, comment=comment)
    return None