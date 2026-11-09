from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func

from app.database import Base


class Student(Base):

    __tablename__ = "students"

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "enrollment_number",
            name="uq_student_department_enrollment"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    enrollment_number = Column(
        String(50),
        nullable=False
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=True,
        unique=True,
        index=True
    )

    phone = Column(
        String(20),
        nullable=True
    )

    date_of_birth = Column(
        Date,
        nullable=True
    )

    gender = Column(
        String(20),
        nullable=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    admission_date = Column(
        Date,
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
        return f"<Student {self.first_name} {self.last_name}>"
    department = relationship("Department", back_populates="students")
    course = relationship("Course", back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student")