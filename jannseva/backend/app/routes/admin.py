@router.get("/admin")
def admin_dashboard(

current_user=Depends(
admin_required
)

):
    return {

"message":"Admin Access"

}