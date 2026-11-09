from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


# Base Schema
class StudentBase(BaseModel):
    enrollment_number: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

    email: str | None = None
    phone: str | None = None

    date_of_birth: date | None = None
    gender: str | None = None

    department_id: int
    course_id: int

    admission_date: date | None = None


# Create Schema
class StudentCreate(StudentBase):
    is_active: bool = True


# Update Schema
class StudentUpdate(BaseModel):
    enrollment_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    email: str | None = None
    phone: str | None = None

    date_of_birth: date | None = None
    gender: str | None = None

    department_id: int | None = None
    course_id: int | None = None

    admission_date: date | None = None
    is_active: bool | None = None


# Response Schema
class StudentResponse(StudentBase):
    id: int
    is_active: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)