from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date, time, datetime


class LectureSessionBase(BaseModel):

    course_id: int
    faculty_id: int

    session_date: date

    start_time: time
    end_time: time

    lecture_number: int = Field(..., gt=0)

    topic: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


class LectureSessionCreate(LectureSessionBase):
    pass


class LectureSessionUpdate(BaseModel):

    course_id: int | None = None
    faculty_id: int | None = None

    session_date: date | None = None

    start_time: time | None = None
    end_time: time | None = None

    lecture_number: int | None = Field(default=None, gt=0)

    topic: str | None = Field(default=None, max_length=255)


class LectureSessionResponse(LectureSessionBase):

    id: int

    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)