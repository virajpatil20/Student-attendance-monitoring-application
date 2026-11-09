from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class LectureSession(Base):
    __tablename__ = "lecture_sessions"

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "session_date",
            "lecture_number",
            name="uq_course_date_lecture"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    faculty_id = Column(
        Integer,
        ForeignKey("faculty.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    session_date = Column(Date, nullable=False, index=True)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    lecture_number = Column(Integer, nullable=False)

    topic = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    course = relationship(
        "Course",
        back_populates="lecture_sessions"
    )

    faculty = relationship(
        "Faculty",
        back_populates="lecture_sessions"
    )

    attendance_records = relationship(
        "Attendance",
        back_populates="lecture_session"
    )

    def __repr__(self):
        return (
            f"<LectureSession Course={self.course_id} "
            f"Date={self.session_date} "
            f"Lecture={self.lecture_number}>"
        )