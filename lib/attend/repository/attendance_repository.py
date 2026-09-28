from datetime import datetime
from typing import Optional
from fastapi import Depends
from lib.attend.core.database import get_db_cursor


class AttendanceRepository:
    def __init__(self, cursor=Depends(get_db_cursor)):
        self.cursor = cursor

    async def record_login(self, staff_id: int) -> int:
        query = """
            INSERT INTO attendance (staff_id, login_time, status)
            VALUES (%s, %s, 'PRESENT')
        """
        # FIX: Added 'await' to cursor.execute
        await self.cursor.execute(query, (staff_id, datetime.now()))
        
        # aiomysql provides lastrowid on the cursor after execute
        return self.cursor.lastrowid

    async def get_active_session(self, staff_id: int) -> Optional[dict]:
        query = """
            SELECT id, staff_id, login_time, logout_time, duration_minutes, status 
            FROM attendance 
            WHERE staff_id = %s AND logout_time IS NULL 
            ORDER BY login_time DESC LIMIT 1
        """
        # FIX: Added 'await' to execute and fetchone
        await self.cursor.execute(query, (staff_id,))
        return await self.cursor.fetchone()

    async def record_logout(self, attendance_id: int, logout_time: datetime, duration_minutes: float):
        query = """
            UPDATE attendance 
            SET logout_time = %s, duration_minutes = %s 
            WHERE id = %s
        """
        # FIX: Added 'await' to cursor.execute
        await self.cursor.execute(query, (logout_time, duration_minutes, attendance_id))

    async def create_leave_request(
        self, staff_id: int, leave_type: str, leave_date, reason: str, status: str
    ) -> int:
        query = """
            INSERT INTO leaves (staff_id, leave_type, leave_date, reason, approval_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        # FIX: Added 'await' to cursor.execute
        await self.cursor.execute(query, (staff_id, leave_type, leave_date, reason, status))
        return self.cursor.lastrowid

    async def update_leave_approval(self, leave_id: int, manager_id: int, status: str):
        query = """
            UPDATE leaves 
            SET approval_status = %s, approved_by = %s 
            WHERE id = %s
        """
        # FIX: Added 'await' to cursor.execute
        await self.cursor.execute(query, (status, manager_id, leave_id))