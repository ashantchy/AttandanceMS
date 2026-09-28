from fastapi import APIRouter, Depends, status
from lib.attend.domain.schemas import (
    LoginRequest, 
    LogoutRequest, 
    RegularLeaveRequest, 
    EmergencyLeaveRequest, 
    LeaveApprovalRequest
)
from lib.attend.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance & Leaves"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def staff_login(
    data: LoginRequest, 
    service: AttendanceService = Depends()
):
    return await service.login(data.email, data.password)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def staff_logout(
    data: LogoutRequest, 
    service: AttendanceService = Depends()
):
    return await service.logout(data.email, data.password)


@router.post("/leave/regular", status_code=status.HTTP_201_CREATED)
async def apply_regular_leave(
    data: RegularLeaveRequest, 
    service: AttendanceService = Depends()
):
    return await service.request_regular_leave(
        data.staff_id, 
        data.leave_date, 
        data.reason
    )


@router.post("/leave/emergency", status_code=status.HTTP_201_CREATED)
async def apply_emergency_leave(
    data: EmergencyLeaveRequest, 
    service: AttendanceService = Depends()
):
    return await service.request_emergency_leave(
        data.staff_id, 
        data.leave_date, 
        data.reason
    )


@router.put("/leave/{leave_id}/approve", status_code=status.HTTP_200_OK)
async def approve_leave(
    leave_id: int, 
    data: LeaveApprovalRequest, 
    service: AttendanceService = Depends()
):
    return await service.approve_leave(
        leave_id, 
        data.manager_id, 
        data.is_approved
    )