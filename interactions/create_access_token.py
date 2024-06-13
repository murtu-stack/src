from datetime import date,datetime,timedelta
from jose import jwt

SECRET_KEY = 'c2c78544f5fafc0673f1d2631c755571c11452d16dedf209060575b9d77ac82a'

ALGORITHM = 'HS256'

def create_access_token(data: dict,expires_delta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
        
    to_encode["exp"] =  expire
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt