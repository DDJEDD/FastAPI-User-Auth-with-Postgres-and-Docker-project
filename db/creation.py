from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    login = Column(String, nullable=False)
    sessions = relationship("Sessions", back_populates="user")


class Sessions(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    device_id = Column(String)
    user = relationship("Users", back_populates="sessions")


