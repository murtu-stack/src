from database.db_session import db
from models.user import User
from models.discussion import Discussion
from models.comment import Comment
from models.comment_like import CommentLike
from models.discussion_like import DiscussionLike
from models.follower_followee import FollowRelation

def create_tables():
    try:
        db.create_tables(
            [FollowRelation]
        )
        db.close()
        print("created tables")
    except:
        print("Exception while creating table")
        raise
