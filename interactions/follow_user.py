
from models.follower_followee import FollowRelation
from models.user import User

def follow_user(follower_id, followee_id):
    follower = User.get_or_none(User.id == follower_id)
    followee = User.get_or_none(User.id == followee_id)

    if follower and followee:
        relation = FollowRelation.select().where(FollowRelation.follower == follower.id, FollowRelation.followee == followee.id).first()
        if relation:
            return {"message" : f"{follower.user_name} already follows {followee.user_name}" }

        FollowRelation.follower = follower.id
        FollowRelation.followee = followee.id
        FollowRelation.save()

        return {"message":  f"{follower.user_name} started following {followee.user_name}"}
    return False