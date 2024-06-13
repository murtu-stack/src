
from fastapi.security import OAuth2PasswordRequestForm
from interactions.authenticate_user import authenticate_user
from fastapi import HTTPException,status,Depends
from interactions.create_access_token import create_access_token
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"user_name": user.get("user_name"),"password": user.get("password")}, expires_delta=access_token_expires)
   
    return {"access_token": access_token, "token_type": "bearer"}