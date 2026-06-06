from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer
from sqlalchemy import String
from pydantic import BaseModel, EmailStr
from app.database import Base

class User(Base):

    __tablename__ = "users"
    id : Mapped[int] = mapped_column( 
           Integer, 
           primary_key=True,
           index=True
    )
    name: Mapped[str] = mapped_column(String)
    
    email: Mapped[str] = mapped_column(
       String, 
       unique=True
    )
    password: Mapped[str] = mapped_column(String)
    
    role: Mapped[str] = mapped_column(
       String, 
       default="user"
    )
    points: Mapped[int] = mapped_column(
       Integer, 
       default=0
    )
    
    
    class UserRegister(BaseModel):

      name:str
      email:EmailStr
      password:str


    class UserLogin(BaseModel):

      email:EmailStr
      password:str


    class UserResponse(BaseModel):

      id:int
      name:str
      email:EmailStr
      role:str
      points:int

    model_config = {"from_attributes": True}