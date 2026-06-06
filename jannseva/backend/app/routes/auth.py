from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.models.user import User, UserRegister, UserLogin
from app.auth.password import hash_password, verify_password
from app.database import get_db

from sqlalchemy.orm import Session
router = APIRouter()

@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    
    existing_user = db.query(User).filter(
    User.email == user.email
).first()

if existing_user:

    raise HTTPException(
        status_code=400,
        detail="Email already exists"
    )

hashed_password = hash_password(
    user.password
)
new_user = User(

    name=user.name,

    email=user.email,

    password=hashed_password
)
db.add(new_user)

db.commit()

db.refresh(new_user)

return {

"message":"User Created"

}
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
    User.email == user.email
).first()
    if not db_user:

    raise HTTPException(
        status_code=401,
        detail="Invalid Credentials"
    )
if not verify_password(
    user.password,
    db_user.password
):

    raise HTTPException(
        status_code=401,
        detail="Invalid Credentials"
    )
token = create_access_token(

{
"id":db_user.id,
"email":db_user.email,
"role":db_user.role
}

)
return {

"access_token":token,

"token_type":"bearer"

}
@router.get("/profile")
def profile(
    current_user=Depends(
        get_current_user
    )
):
    return current_user
def admin_required(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] != "admin":

    raise HTTPException(
        status_code=403,
        detail="Admin Only"
    )

return current_user