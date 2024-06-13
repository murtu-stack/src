from datetime import datetime
from database.base_model import BaseModel
from playhouse.postgres_ext import (
    BigAutoField,
    CharField,
    DateTimeField,
    BigIntegerField
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
        
def get_hash_password(plain_password):
    return pwd_context.hash(plain_password)
    
    
class User(BaseModel):
    id = BigAutoField(primary_key=True)
    user_name = CharField()
    email = CharField()
    password = CharField()
    first_name = CharField(null =True)
    last_name = CharField(null =True)
    mobile_number = BigIntegerField(null=True)
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())
    
    
        
    class Meta:
        table_name = 'users'
        
    
        
    
    
    
        
        