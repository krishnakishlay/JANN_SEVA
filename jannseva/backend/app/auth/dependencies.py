from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
from jose import jwt

def get_current_user(
    token:str = Depends(oauth2_scheme)
):
    payload = jwt.decode(

token,

SECRET_KEY,

algorithms=[ALGORITHM]

)
    user_id = payload.get("id")
    return payload