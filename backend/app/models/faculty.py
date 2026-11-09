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


class Faculty(Base):

    __tablename__ = "faculty"

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "employee_code",
            name="uq_faculty_department_employee"
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

    employee_code = Column(
        String(30),
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
        nullable=False,
        unique=True,
        index=True
    )

    phone = Column(
        String(20),
        nullable=True
    )

    designation = Column(
        String(100),
        nullable=True
    )

    specialization = Column(
        String(255),
        nullable=True
    )

    qualification = Column(
        String(255),
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
        return f"<Faculty {self.first_name} {self.last_name}>"
    department = relationship("Department", back_populates="faculty_members")
    lecture_sessions = relationship(
    "LectureSession",
    back_populates="faculty"
)