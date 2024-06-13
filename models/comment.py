from database.base_model import BaseModel
from datetime import datetime
from playhouse.postgres_ext import (
    DateTimeField,
    ForeignKeyField,
    TextField
)

from models.user import User
from models.discussion import Discussion

class Comment(BaseModel):
    user = ForeignKeyField(User, backref='comments')
    discussion = ForeignKeyField(Discussion, backref='comments')
    text = TextField()
    created_on = DateTimeField(default=datetime.now)
    parent = ForeignKeyField('self', null=True, backref='replies')