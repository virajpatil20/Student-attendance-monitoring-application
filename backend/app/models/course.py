from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func

from app.database import Base


class Course(Base):

    __tablename__ = "courses"

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "code",
            name="uq_course_department_code"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    code = Column(
        String(30),
        nullable=False
    )

    degree_level = Column(
        String(50),
        nullable=True
    )

    duration_years = Column(
        Integer,
        nullable=True
    )

    description = Column(
        String(500),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
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

    def __repr__(self):
        return f"<Course {self.name}>"
    department = relationship("Department", back_populates="courses")
    students = relationship("Student", back_populates="course")
    lecture_sessions = relationship(
    "LectureSession",
    back_populates="course"
)