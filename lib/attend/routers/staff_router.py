from fastapi import APIRouter, Depends, status
from lib.attend.domain.schemas import StaffCreate
from lib.attend.services.staff_service import StaffService

router = APIRouter(prefix="/staff", tags=["Staff Management"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_staff(
    data: StaffCreate, 
    staff_service: StaffService = Depends()
):
    staff_id = await staff_service.create_staff(data)
    return {
        "message": "Staff member created successfully", 
        "staff_id": staff_id
    }