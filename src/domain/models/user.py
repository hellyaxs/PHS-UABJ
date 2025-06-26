from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from src.infra.config.database.database import Base

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 