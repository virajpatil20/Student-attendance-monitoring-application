from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


# Base Schema
class AttendanceBase(BaseModel):

    student_id: int
    course_id: int
    faculty_id: int | None = None

    attendance_date: date

    status: str = Field(..., min_length=1, max_length=20)

    remarks: str | None = Field(default=None, max_length=500)


# Create Schema
class AttendanceCreate(AttendanceBase):
    pass


# Update Schema
class AttendanceUpdate(BaseModel):

    student_id: int | None = None
    course_id: int | None = None
    faculty_id: int | None = None

    attendance_date: date | None = None

    status: str | None = Field(default=None, max_length=20)

    remarks: str | None = Field(default=None, max_length=500)


# Response Schema
class AttendanceResponse(AttendanceBase):

    id: int

    marked_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
    