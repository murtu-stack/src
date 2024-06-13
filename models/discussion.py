from datetime import datetime
from libs.enums import DocumentStateEnum
from database.base_model import BaseModel
from playhouse.postgres_ext import (
    BigAutoField,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
    TextField,
    ArrayField
)
from models.user import User

class Discussion(BaseModel):
    user = ForeignKeyField(User, backref='discussions')
    text = TextField()
    image = CharField(null=True)
    hashtags = ArrayField(CharField)
    created_on = DateTimeField(default=datetime.now)
    view_count = IntegerField(default=0)
