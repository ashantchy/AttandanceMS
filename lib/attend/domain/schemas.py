from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date

# --- Staff Schemas ---
class StaffCreate(BaseModel):
  name: str
  email: str
  password: str = Field(..., max_length=72, description="Password must be at most 72 characters")
  department: str
  role: str = "staff"
  
class StaffResponse(StaffCreate):
  id: int
  created_at: datetime
  
# --- Attendance Schemas ---
class LoginRequest(BaseModel):
  email: EmailStr
  password: str = Field(..., max_length=72)
  
class LogoutRequest(BaseModel):
  email: EmailStr
  password: str = Field(..., max_length=72)
  
class AttendanceResponse(BaseModel):
  id: int
  staff_id: int
  login_time: datetime
  logout_time: Optional[datetime] = None
  duration_minutes: Optional[float] = None
  status: str
  
# --- Leave Schemas ---
class RegularLeaveRequest(BaseModel):
  staff_id: int
  leave_date: date
  reason: str
  
class EmergencyLeaveRequest(BaseModel):
  staff_id: int
  leave_date: date
  reason: str
  
class LeaveApprovalRequest(BaseModel):
  manager_id: int
  is_approved: bool
  
class LeaveResponse(BaseModel):
  id: int
  staff_id: int
  leave_type: str
  leave_date: date
  reason: str
  approval_status: str
  approved_by: Optional[int] = None