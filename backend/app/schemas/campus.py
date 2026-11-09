from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CampusBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=30)

    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)

    institution_id: int


class CampusCreate(CampusBase):
    is_active: bool = True


class CampusUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=30)

    address: str | None = Field(None, max_length=500)
    city: str | None = Field(None, max_length=100)
    state: str | None = Field(None, max_length=100)
    pincode: str | None = Field(None, max_length=10)

    institution_id: int | None = None
    is_active: bool | None = None


class CampusResponse(CampusBase):
    id: int
    is_active: bool

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)