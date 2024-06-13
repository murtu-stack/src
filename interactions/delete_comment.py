from interactions.get_comment import get_comment

def delete_comment(comment_id):
    comment = get_comment(comment_id)
    if comment:
        comment.delete_instance()
        return True
    return False