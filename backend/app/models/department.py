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


class Department(Base):

    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint(
            "campus_id",
            "code",
            name="uq_department_campus_code"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    campus_id = Column(
        Integer,
        ForeignKey("campuses.id", ondelete="RESTRICT"),
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

    description = Column(
        String(500),
        nullable=True
    )

    hod_name = Column(
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
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Department {self.name}>"
    
    campus = relationship("Campus", back_populates="departments")
    courses = relationship("Course", back_populates="department")
    faculty_members = relationship("Faculty", back_populates="department")
    students = relationship("Student", back_populates="department")