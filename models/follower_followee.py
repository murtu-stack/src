from playhouse.postgres_ext import ForeignKeyField
from models.user import User
from database.base_model import BaseModel

class FollowRelation(BaseModel):
    follower = ForeignKeyField(User, backref='following_relations')
    followee = ForeignKeyField(User, backref='follower_relations')
