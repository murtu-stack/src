from interactions.get_comment import get_comment

def update_comment(comment_id, comment_data):
    comment = get_comment(comment_id)
    if comment:
        for key, value in comment_data.items():
            setattr(comment, key, value)
        comment.save()
        return comment
    return None