from models.comment import Comment

def get_comment(comment_id):
    return Comment.get_or_none(Comment.id == comment_id)