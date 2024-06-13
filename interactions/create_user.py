
from models.user import User
from pydantic import  BaseModel
from fastapi import HTTPException,status
from interactions.create_access_token import create_access_token
from passlib.context import CryptContext


def create_user(request:dict):
    user = User.select().where(User.user_name == request.get("user_name")).first()
    if user:
        raise HTTPException(status_code=400, detail="user name already exist")
    initialize_params = {key: val  for key,val in request.items() if key in ["user_name","email"]}
    user =User(**initialize_params)
    
    context = CryptContext(schemes=['bcrypt'])
    password = context.hash(request.get("password"))
    request["password"] = password
    for key,val in request.items():
        setattr(user,key,val)
    
    
    with User._meta.database.atomic():
        try:
            user.save()
            return create_access_token(data = {"user_name": user.user_name, "password": user.password})
        except:
            raise
        