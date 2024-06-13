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
from models.discussion import Discussion


class DiscussionLike(BaseModel):
    user = ForeignKeyField(User, backref='likes')
    discussion = ForeignKeyField(Discussion, backref='likes')