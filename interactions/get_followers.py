from models.user import User
from models.follower_followee import FollowRelation
def get_followers(user_id):
    user = User.get_or_none(User.id == user_id)
    if user:
        return [relation.follower for relation in user.follower_relations]
    return None
