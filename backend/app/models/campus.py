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
from sqlalchemy.orm import relationship

from app.database import Base


class Campus(Base):

    __tablename__ = "campuses"

    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "code",
            name="uq_campus_institution_code"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    institution_id = Column(
        Integer,
        ForeignKey("institutions.id", ondelete="RESTRICT"),
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

    address = Column(
        String(500),
        nullable=True
    )

    city = Column(
        String(100),
        nullable=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    pincode = Column(
        String(10),
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

    # Relationships
    institution = relationship(
        "Institution",
        back_populates="campuses"
    )

    def __repr__(self):
        return f"<Campus {self.name}>"
    
    departments = relationship("Department", back_populates="campus")