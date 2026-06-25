from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.routes.auth import admin_required
from app.schemas.admin import StatusUpdate

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    total_users = db.query(User).count()
    total_complaints = db.query(Complaint).count()
    pending_complaints = db.query(Complaint).filter(Complaint.status == "Pending").count()
    resolved_complaints = db.query(Complaint).filter(Complaint.status == "Resolved").count()

    return {
        "total_users": total_users,
        "total_complaints": total_complaints,
        "pending_complaints": pending_complaints,
        "resolved_complaints": resolved_complaints
    }

@router.get("/complaints")
def get_all_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    complaints = db.query(Complaint).all()
    return complaints

@router.get("/complaints/{complaint_id}")
def complaint_details(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.put("/complaints/{complaint_id}/status")
def update_status(
    complaint_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    complaint.status = data.status
   
    if data.status == "Resolved":
       user = db.query(User).filter(User.id == complaint.user_id).first()
       user.points += 20
    db.commit()
    db.refresh(complaint)
    
    return {
        "message": "Status updated successfully"
    }



@router.delete("/complaints/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    db.delete(complaint)
    db.commit()
    
    return {
        "message": "Complaint deleted successfully"
    }

@router.get("/complaints")
def get_complaints(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    query = db.query(Complaint)
    if status:
        query = query.filter(Complaint.status == status)
    complaints = query.all()
    return complaints