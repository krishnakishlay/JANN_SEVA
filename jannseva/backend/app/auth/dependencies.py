from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt
from app.auth.jwt_handler import(SECRET_KEY,ALGORITHM)
from fastapi import HTTPException

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

def admin_required(
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user