from typing import Optional
from fastapi import Depends
from lib.attend.domain.models import Staff
from lib.attend.core.database import get_db_cursor

class StaffRepository:
    def __init__(self, cursor=Depends(get_db_cursor)):
        self.cursor = cursor

    async def create(self, staff: Staff) -> int:
        query = """
            INSERT INTO staff (name, email, password_hash, department, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        await self.cursor.execute(
            query, (staff.name, staff.email, staff.password_hash, staff.department, staff.role)
        )
        return self.cursor.lastrowid

    async def get_by_email(self, email: str) -> Optional[dict]:
        query = "SELECT * FROM staff WHERE email = %s"
        await self.cursor.execute(query, (email,))
        return await self.cursor.fetchone()

    async def get_by_id(self, staff_id: int) -> Optional[dict]:
        query = "SELECT * FROM staff WHERE id = %s"
        await self.cursor.execute(query, (staff_id,))
        return await self.cursor.fetchone()