from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Base Schema
class AdminBase(BaseModel):

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)

    role: str = "admin"


# Create Schema
class AdminCreate(AdminBase):

    password: str = Field(..., min_length=8)


# Update Schema
class AdminUpdate(BaseModel):

    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)

    email: str | None = Field(default=None, max_length=255)

    password: str | None = Field(default=None, min_length=8)

    role: str | None = None
    is_active: bool | None = None


# Response Schema
class AdminResponse(AdminBase):

    id: int
    is_active: bool

    last_login_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)