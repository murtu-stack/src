
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends
from jose import jwt
from jose import JWTError
from models.user import User
from fastapi import HTTPException,status
from interactions.authenticate_user import authenticate_user

SECRET_KEY = 'c2c78544f5fafc0673f1d2631c755571c11452d16dedf209060575b9d77ac82a'

ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token : str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      
        username = payload.get("user_name")
        password = payload.get("password")
        if username is None:
            raise credential_exception
     
    except JWTError:
        raise credential_exception
    

    return {"is_authorized": True,"user_name": username}
