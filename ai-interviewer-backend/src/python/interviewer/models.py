from sqlalchemy import Column, Integer, String
from .database import Base
from .schemas import User


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    name = Column(String, index=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, index=False)

    def to_user(self) -> User:
        return User(user_id=self.user_id,
                    name=self.name,
                    email=self.email,
                    password=self.password_hash)
