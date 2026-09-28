from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, Date, ForeignKey, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# =====================================================================
# 1. Pure Domain Entities (Used by Routers, Services & Domain Logic)
# =====================================================================

@dataclass
class Staff:
    id: Optional[int]
    name: str
    email: str
    department: str
    password_hash: str  # Added field
    role: str = "staff"
    created_at: Optional[datetime] = None


@dataclass
class Attendance:
    id: Optional[int]
    staff_id: int
    login_time: datetime
    logout_time: Optional[datetime] = None
    duration_minutes: Optional[float] = None
    status: str = "PRESENT"

    def calculate_logout(self, logout_time: datetime) -> float:
        """Domain logic method inside the Entity."""
        if self.logout_time is not None:
            raise ValueError("Session is already logged out.")
        self.logout_time = logout_time
        duration = round((logout_time - self.login_time).total_seconds() / 60, 2)
        self.duration_minutes = duration
        return duration


@dataclass
class Leave:
    id: Optional[int]
    staff_id: int
    leave_type: str  # 'REGULAR' or 'EMERGENCY'
    leave_date: date
    reason: str
    approval_status: str  # 'PENDING', 'APPROVED', 'REJECTED', 'AUTO_APPROVED'
    approved_by: Optional[int] = None
    created_at: Optional[datetime] = None


# =====================================================================
# 2. SQLAlchemy ORM Models (Used exclusively by Alembic --autogenerate)
# =====================================================================

class StaffModel(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # Added column
    department = Column(String(50), nullable=False)
    role = Column(String(20), server_default="staff")
    created_at = Column(DateTime, server_default=func.now())


class AttendanceModel(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Float, nullable=True)
    status = Column(String(20), server_default="PRESENT")


class LeaveModel(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    leave_type = Column(Enum("REGULAR", "EMERGENCY"), nullable=False)
    leave_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    approval_status = Column(Enum("PENDING", "APPROVED", "REJECTED", "AUTO_APPROVED"), server_default="PENDING")
    approved_by = Column(Integer, ForeignKey("staff.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())