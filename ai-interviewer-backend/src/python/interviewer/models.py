from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from interviewer.app.api.schemas.user import User


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


class InterviewModel(Base):
    __tablename__ = "interviews"

    interview_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    topic = Column(String, index=False)
    user_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    state = Column(String, index=True)


class InterviewChatModel(Base):
    __tablename__ = "interview_chats"

    chat_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    interview_id = Column(Integer, index=True)
    sequence_no = Column(Integer, index=False)
    participant_type = Column(String, index=False)
    message = Column(String, index=False)
    message_type = Column(String, index=False)
