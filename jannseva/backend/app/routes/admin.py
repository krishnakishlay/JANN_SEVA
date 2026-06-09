from fastapi import APIRouter, Depends
from app.routes.auth import admin_required
from typing import Any

router = APIRouter()

@router.get("/admin")
def admin_dashboard(

current_user: Any=
Depends(admin_required)

):
    return {

"message":"Admin Access"

}