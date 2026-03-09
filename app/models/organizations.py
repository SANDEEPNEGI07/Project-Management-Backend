from sqlalchemy import Column, Integer, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.core.enums import OrganizationStatus


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(OrganizationStatus), nullable=False, default=OrganizationStatus.ACTIVE)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("ProjectModel", back_populates="organization", passive_deletes=False)
