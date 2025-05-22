from sqlalchemy import Column, Integer, String
from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    name = Column(String, index=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(Integer, index=False)
