from fastapi import FastAPI

from app.database import Base, engine
import app.models

# Import API routers
from app.routers import (
    admin,
    attendance,
    campus,
    course,
    department,
    faculty,
    institution,
    student,
    lecture_session,
)

app = FastAPI(
    title="Smart Attendance System",
    version="1.0.0",
)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Smart Attendance API is running!"
    }


# Register API routers
app.include_router(admin.router)
app.include_router(attendance.router)
app.include_router(campus.router)
app.include_router(course.router)
app.include_router(department.router)
app.include_router(faculty.router)
app.include_router(institution.router)
app.include_router(student.router)
app.include_router(lecture_session.router)