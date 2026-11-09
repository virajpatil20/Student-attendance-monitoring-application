from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Base Schema
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=30)

    campus_id: int

    description: str | None = Field(default=None, max_length=500)
    hod_name: str | None = Field(default=None, max_length=255)


# Create Schema
class DepartmentCreate(DepartmentBase):
    is_active: bool = True


# Update Schema
class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    code: str | None = Field(default=None, max_length=30)

    campus_id: int | None = None

    description: str | None = Field(default=None, max_length=500)
    hod_name: str | None = Field(default=None, max_length=255)

    is_active: bool | None = None


# Response Schema
class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)