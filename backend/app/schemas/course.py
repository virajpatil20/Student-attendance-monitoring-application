from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Base Schema
class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=30)

    department_id: int

    degree_level: str | None = Field(default=None, max_length=50)
    duration_years: int | None = Field(default=None, ge=1)

    description: str | None = Field(default=None, max_length=500)


# Create Schema
class CourseCreate(CourseBase):
    is_active: bool = True


# Update Schema
class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    code: str | None = Field(default=None, max_length=30)

    department_id: int | None = None

    degree_level: str | None = Field(default=None, max_length=50)
    duration_years: int | None = Field(default=None, ge=1)

    description: str | None = Field(default=None, max_length=500)

    is_active: bool | None = None


# Response Schema
class CourseResponse(CourseBase):
    id: int
    is_active: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)