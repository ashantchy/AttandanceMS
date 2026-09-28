from fastapi import FastAPI
import uvicorn
from lib.attend.routers.staff_router import router as staff_router
from lib.attend.routers.attendance_router import router as attendance_router

app = FastAPI(title="Attendance Management System")

# Modular router inclusions
app.include_router(staff_router)
app.include_router(attendance_router)

