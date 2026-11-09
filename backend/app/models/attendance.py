from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "session_id",
            name="uq_student_lecture_attendance"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("lecture_sessions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        nullable=False
    )

    remarks = Column(
        String(500),
        nullable=True
    )

    marked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    student = relationship(
        "Student",
        back_populates="attendance_records"
    )

    lecture_session = relationship(
        "LectureSession",
        back_populates="attendance_records"
    )

    def __repr__(self):
        return (
            f"<Attendance student_id={self.student_id} "
            f"session_id={self.session_id} "
            f"status={self.status}>"
        )