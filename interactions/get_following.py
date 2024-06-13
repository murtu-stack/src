from models.user import User

def get_following(user_id):
    user = User.get_or_none(User.id == user_id)
    if user:
        return [relation.followee for relation in user.following_relations]
    return None
