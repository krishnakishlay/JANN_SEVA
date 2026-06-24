from fastapi import File, Form, UploadFile
from pydantic import BaseModel

class ComplaintCreate(BaseModel):

    title: str = Form(...)

    description: str = Form(...)

    category: str = Form(...)

    location: str = Form(...)

    image: UploadFile = File(...)

    class ComplaintResponse(BaseModel):

     id: int

    title: str

    description: str

    category: str

    status: str

    location: str

    class Config:
        from_attributes = True

class ComplaintUpdate(BaseModel):

    title: str

    description: str

    category: str

    location:str       