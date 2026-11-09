from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Base Schema
class FacultyBase(BaseModel):
    department_id: int

    employee_code: str = Field(
        ..., min_length=1, max_length=30
    )

    first_name: str = Field(
        ..., min_length=1, max_length=100
    )

    last_name: str = Field(
        ..., min_length=1, max_length=100
    )

    email: str = Field(
        ..., min_length=1, max_length=255
    )

    phone: str | None = Field(
        default=None, max_length=20
    )

    designation: str | None = Field(
        default=None, max_length=100
    )

    specialization: str | None = Field(
        default=None, max_length=255
    )

    qualification: str | None = Field(
        default=None, max_length=255
    )


# Create Schema
class FacultyCreate(FacultyBase):
    is_active: bool = True


# Update Schema
class FacultyUpdate(BaseModel):
    department_id: int | None = None

    employee_code: str | None = Field(
        default=None, max_length=30
    )

    first_name: str | None = Field(
        default=None, max_length=100
    )

    last_name: str | None = Field(
        default=None, max_length=100
    )

    email: str | None = Field(
        default=None, max_length=255
    )

    phone: str | None = Field(
        default=None, max_length=20
    )

    designation: str | None = Field(
        default=None, max_length=100
    )

    specialization: str | None = Field(
        default=None, max_length=255
    )

    qualification: str | None = Field(
        default=None, max_length=255
    )

    is_active: bool | None = None


# Response Schema
class FacultyResponse(FacultyBase):
    id: int
    is_active: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)