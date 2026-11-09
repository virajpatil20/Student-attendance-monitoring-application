from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Base Schema
class InstitutionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=20)
    description: str | None = Field(default=None, max_length=500)


# Create Schema
class InstitutionCreate(InstitutionBase):
    is_active: bool = True


# Update Schema
class InstitutionUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    code: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool | None = None


# Response Schema
class InstitutionResponse(InstitutionBase):
    id: int
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)