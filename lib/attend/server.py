from fastapi import FastAPI

from lib.attend.routers.attendance_router import router as attendance_router
from lib.attend.routers.staff_router import router as staff_router

app = FastAPI(title="Attendance Management System")
app.include_router(staff_router)
app.include_router(attendance_router)


@app.get("/")
async def root():
	return {"message": "Attend API is running"}