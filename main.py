# import click
# import uvicorn


# @click.command()
# @click.option(
#     '--mode',
#     type=click.Choice(
#         ['attend_prd', 'attend_dev', 'manual'],
#         case_sensitive=False
#     ),
#     help="Run the app in production, development, or manual mode."
# )
# def main(mode):
#     match mode.lower():
#         case 'attend_prd':
#             print("Running the API in production mode...")
#             uvicorn.run(
#                 'lib.attend.server:app',
#                 host="0.0.0.0"
#             )

#         case 'attend_dev':
#             print("Running the API in development mode...")
#             uvicorn.run(
#                 'lib.attend.server:app',
#                 host="0.0.0.0",
#                 reload=True
#             )

#         case 'manual':
#             print("Running in MANUAL mode...")


# if __name__ == "__main__":
#     main()

from fastapi import FastAPI
import uvicorn

from lib.attend.routers.staff_router import router as staff_router
from lib.attend.routers.attendance_router import router as attendance_router

app = FastAPI(title="Attendance Management System")

# Modular router inclusions
app.include_router(staff_router)
app.include_router(attendance_router)

# Optional alias (keep only if required by your deployment interface)
# application = app


@app.get("/")
async def root():
    return {
        "message": "Attend API is running"
    }


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)