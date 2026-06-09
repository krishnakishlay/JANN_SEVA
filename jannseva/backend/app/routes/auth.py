from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user import UserRegister
from app.schemas.user import UserLogin

from app.auth.password import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)

from app.auth.dependencies import (
    get_current_user
)

from app.database import get_db

from typing import Any

router = APIRouter()


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

  try:

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
        "message": "User Created"
    }
    
  except Exception as e:
    print("REGISTER ERROR:",repr(e))
    raise

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
        str(db_user.password)
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    token = create_access_token(
        {
            "id": db_user.id,
            "email": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/profile")
def profile(
    current_user: Any=Depends(
        get_current_user
    )
):
    return current_user


def admin_required(
    current_user: Any=Depends(
        get_current_user
    )
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin Only"
        )

    return current_user