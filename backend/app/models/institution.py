from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Institution(Base):

    __tablename__ = "institutions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False,
        unique=True
    )

    code = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True
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

    # Relationships
    campuses = relationship(
        "Campus",
        back_populates="institution"
    )

    def __repr__(self):
        return f"<Institution {self.name}>"