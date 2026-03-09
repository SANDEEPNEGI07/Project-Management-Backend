from app.db.base import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    username = Column(Text, nullable=False)
    firstName = Column(Text, nullable=True)
    lastName = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    avatarUrl = Column(Text, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="profile")
