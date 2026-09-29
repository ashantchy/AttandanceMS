# from fastapi import FastAPI
# import uvicorn

# from lib.attend.routers.staff_router import router as staff_router
# from lib.attend.routers.attendance_router import router as attendance_router

# app = FastAPI(title="Attendance Management System")

# # Modular router inclusions
# app.include_router(staff_router)
# app.include_router(attendance_router)

# # Optional alias (keep only if required by your deployment interface)
# # application = app


# @app.get("/")
# async def root():
#     return {
#         "message": "Attend API is running"
#     }


# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)