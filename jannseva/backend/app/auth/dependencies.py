from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt
from app.auth.jwt_handler import(SECRET_KEY,ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_current_user(
    token:str = Depends(oauth2_scheme)
):
    payload = jwt.decode(

token,

SECRET_KEY,

algorithms=[ALGORITHM]

)
    return payload