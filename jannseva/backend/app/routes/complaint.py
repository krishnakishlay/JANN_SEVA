from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.complaint import ComplaintCreate
from app.auth.dependencies import get_current_user
from typing import Dict,Any

router = APIRouter(
prefix="/complaints",
tags=["Complaints"]
)

@router.post("/")
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str,Any] =
    Depends(get_current_user)
):
    
    user = db.query(User).filter(
        User.id == current_user["id"]
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail ="User not found"
        )
    
    new_complaint = Complaint(
            title=complaint.title,
            description=complaint.description,
            category=complaint.category,
            location=complaint.location,
            user_id= user.id
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    user.point += 10
    db.commit()
    
    return 
    {
    "message": "Complaint Created",
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
