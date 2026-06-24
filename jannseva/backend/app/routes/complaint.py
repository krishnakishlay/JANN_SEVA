from fastapi import APIRouter, Form
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File
from app.services.cloudinary import upload_image
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.complaint import ComplaintUpdate
from app.auth.dependencies import get_current_user
from typing import Dict, Any
import os


router = APIRouter(
prefix="/complaints",
tags=["Complaints"]
)

@router.post("/")
def create_complaint(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Dict[str,Any] =Depends(get_current_user)
):

    temp_file = f"temp_{image.filename}"

    with open(temp_file, "wb") as buffer:
        buffer.write(image.file.read())
    
    image_url = upload_image(temp_file)
    
    os.remove(temp_file)

    
    user = db.query(User).filter(
        User.id == current_user["id"]
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail ="User not found"
        )
    



    
    new_complaint = Complaint(
        title=title,
        description=description,
        category=category,
        location=location,
        image_url=image_url,
        user_id=current_user["id"]
    )


    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    user.points += 10
    db.commit()
    


    return {
        "message": "Complaint Created",
        "image_url": image_url,
        "points_earned": 10,
        "complaint_id": new_complaint.id
    }


@router.get("/")
def get_complaints(
   db: Session = Depends(get_db),
   current_user: Dict[str, Any] = 
   Depends(get_current_user)
):
    complaints = db.query(
    Complaint
).filter(
    Complaint.user_id == current_user["id"]
).all()
    return complaints

@router.get("/{complaint_id}")
def get_complaint(
   complaint_id:int,
   db: Session = Depends(get_db),
   current_user: Dict[str, Any] =
   Depends(get_current_user)
):
    complaint = db.query(
    Complaint
).filter(
    Complaint.id == complaint_id
).first()
    
    if not complaint:
     raise HTTPException(
        status_code=404,
        detail="Complaint not found"
    )

    return complaint

@router.put("/{complaint_id}")
def update_complaint(
    complaint_id:int,
    updated_data: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] =
    Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )
    complaint_obj: Any = complaint
    complaint_obj.title = updated_data.title
    complaint_obj.description = updated_data.description
    complaint_obj.category = updated_data.category
    complaint_obj.location = updated_data.location
    db.commit()
    db.refresh(complaint)
    return {
        "message": "Complaint Updated",
    }

@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id:int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] =
    Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )
    db.delete(complaint)
    db.commit()
    return {
        "message": "Complaint Deleted"
    }



