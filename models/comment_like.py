from datetime import datetime
from database.base_model import BaseModel
from playhouse.postgres_ext import (
    BigAutoField,
    CharField,
    ForeignKeyField,
    DateTimeField,
    BigIntegerField
)
from models.user import User
from models.comment import Comment

class CommentLike(BaseModel):
    user = ForeignKeyField(User, backref='comment_likes')
    comment = ForeignKeyField(Comment, backref='likes')
