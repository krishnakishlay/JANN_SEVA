from pydantic import BaseModel

class ComplaintCreate(BaseModel):

    title: str

    description: str

    category: str

    location: str

    class ComplaintResponse(BaseModel):

     id: int

    title: str

    description: str

    category: str

    status: str

    location: str

    class Config:
        from_attributes = True