
from models.user import User
from models.follower_followee import FollowRelation
def unfollow_user(follower_id, followee_id):
    relation = FollowRelation.get_or_none(FollowRelation.follower_id == follower_id, FollowRelation.followee_id == followee_id)
    if relation:
        relation.delete_instance()
        return True
    return False
