from models.user import User
from models.user import verify_password,get_hash_password
from fastapi.encoders import jsonable_encoder

def authenticate_user(user_name,password):
    
    user = User.select().where(User.user_name == user_name).first()
    if not user:
        return False
    
    if not verify_password(password,user.password):
        return False
    return jsonable_encoder(user.__data__)
        