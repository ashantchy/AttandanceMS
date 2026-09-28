from fastapi import Depends, HTTPException
from lib.attend.domain.schemas import StaffCreate
from lib.attend.domain.models import Staff
from lib.attend.repository.staff_repository import StaffRepository
from lib.attend.services.security import hash_password

class StaffService:
    def __init__(self, staff_repo: StaffRepository = Depends()):
        self.staff_repo = staff_repo

    async def create_staff(self, data: StaffCreate) -> int:
        existing = await self.staff_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pwd = hash_password(data.password)

        staff_entity = Staff(
            id=None,
            name=data.name,
            email=data.email,
            password_hash=hashed_pwd,
            department=data.department,
            role=data.role
        )
        return await self.staff_repo.create(staff_entity)