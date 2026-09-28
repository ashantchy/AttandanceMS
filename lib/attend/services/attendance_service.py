from datetime import datetime
from fastapi import Depends, HTTPException
from lib.attend.repository.staff_repository import StaffRepository
from lib.attend.repository.attendance_repository import AttendanceRepository
from lib.attend.domain.models import Attendance
from lib.attend.services.security import verify_password


class AttendanceService:
    def __init__(
        self, 
        attendance_repo: AttendanceRepository = Depends(),
        staff_repo: StaffRepository = Depends()
    ):
        self.attendance_repo = attendance_repo
        self.staff_repo = staff_repo

    # =========================================================================
    # Attendance Operations
    # =========================================================================

    async def login(self, email: str, password: str):
        # 1. Authenticate credentials
        staff = await self.staff_repo.get_by_email(email)
        if not staff or not verify_password(password, staff["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        staff_id = staff["id"]

        # 2. Check for existing active session
        active_session = await self.attendance_repo.get_active_session(staff_id)
        if active_session:
            raise HTTPException(status_code=400, detail="Staff member is already logged in")

        # 3. Create session
        attendance_id = await self.attendance_repo.record_login(staff_id)
        return {
            "message": "Login successful", 
            "email": email, 
            "attendance_id": attendance_id
        }

    async def logout(self, email: str, password: str):
        # 1. Authenticate credentials
        staff = await self.staff_repo.get_by_email(email)
        if not staff or not verify_password(password, staff["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        staff_id = staff["id"]

        # 2. Find active session
        raw_session = await self.attendance_repo.get_active_session(staff_id)
        if not raw_session:
            raise HTTPException(status_code=400, detail="No active login session found for this account")

        # 3. Execute domain logic calculation
        attendance = Attendance(
            id=raw_session["id"],
            staff_id=raw_session["staff_id"],
            login_time=raw_session["login_time"]
        )

        if attendance.id is None:
            raise HTTPException(status_code=500, detail="Invalid attendance record ID")

        logout_time = datetime.now()
        duration_minutes = attendance.calculate_logout(logout_time)

        # Pyright now knows attendance.id is strictly int
        await self.attendance_repo.record_logout(attendance.id, logout_time, duration_minutes)

        return {
            "message": "Logout successful",
            "email": email,
            "login_time": attendance.login_time,
            "logout_time": logout_time,
            "duration_minutes": duration_minutes
        }

    # =========================================================================
    # Leave Operations (Converted to async/await)
    # =========================================================================

    async def request_regular_leave(self, staff_id: int, leave_date, reason: str):
        staff = await self.staff_repo.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")

        leave_id = await self.attendance_repo.create_leave_request(
            staff_id=staff_id,
            leave_type="REGULAR",
            leave_date=leave_date,
            reason=reason,
            status="PENDING"
        )
        return {
            "message": "Regular leave requested. Pending manager approval.",
            "leave_id": leave_id
        }

    async def request_emergency_leave(self, staff_id: int, leave_date, reason: str):
        staff = await self.staff_repo.get_by_id(staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")

        leave_id = await self.attendance_repo.create_leave_request(
            staff_id=staff_id,
            leave_type="EMERGENCY",
            leave_date=leave_date,
            reason=reason,
            status="AUTO_APPROVED"
        )
        return {
            "message": "Emergency leave auto-approved. No manager approval needed.",
            "leave_id": leave_id
        }

    async def approve_leave(self, leave_id: int, manager_id: int, is_approved: bool):
        manager = await self.staff_repo.get_by_id(manager_id)
        if not manager or manager.get("role") != "manager":
            raise HTTPException(status_code=403, detail="Only managers can approve leave requests")

        status = "APPROVED" if is_approved else "REJECTED"
        await self.attendance_repo.update_leave_approval(leave_id, manager_id, status)
        return {
            "message": f"Leave status updated to {status} by manager ID {manager_id}",
            "leave_id": leave_id
        }