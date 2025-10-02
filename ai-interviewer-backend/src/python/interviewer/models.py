from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .app.api.schemas.AssessmentItem import AssessmentItem
from .app.api.schemas.Interview import Interview
from .app.api.schemas.InterviewState import InterviewState
from .app.api.schemas.Question import Question
from .database import Base
from interviewer.app.api.schemas.user import User


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    name = Column(String, index=False)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, index=False)

    def to_user(self) -> User:
        return User(user_id=int(self.user_id),
                    name=self.name,
                    email=self.email,
                    password=self.password_hash)


class InterviewModel(Base):
    __tablename__ = "interviews"

    interview_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    topic = Column(String, index=False)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime, index=True, server_default=func.now())
    end_time = Column(DateTime, index=True)
    state = Column(String, index=True)
    number_of_questions = Column(Integer, index=False)
    number_of_follow_up_questions = Column(Integer, index=False)

    def to_interview(self) -> Interview:
        return Interview(
            interview_id=int(self.interview_id),
            user_id=int(self.user_id),
            topic=self.topic,
            start_time=self.start_time,
            end_time=self.end_time,
            state=InterviewState.from_str(self.state),
            number_of_questions=int(self.number_of_questions),
            number_of_follow_up_questions=int(self.number_of_follow_up_questions),
        )


class AssessmentItemModel(Base):
    __tablename__ = "assessment_items"

    item_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    interview_id = Column(Integer, index=True)
    sequence_no = Column(Integer, index=False)
    part_no = Column(Integer, index=False)
    question_id = Column(Integer, index=True)
    question = Column(String, index=False)
    answer = Column(String, index=False, nullable=True)
    evaluation_log = Column(String, index=False, nullable=True)
    score = Column(Integer, index=False, nullable=True)

    def to_assessment_item(self) -> AssessmentItem:
        return AssessmentItem(
            item_id=int(self.item_id),
            interview_id=int(self.interview_id),
            sequence_no=int(self.sequence_no),
            part_no=int(self.part_no),
            question_id=int(self.question_id),
            question=self.question,
            answer=self.answer,
            evaluation_log=self.evaluation_log,
            score=int(self.score) if self.score else 0,
        )

class QuestionsModel(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    part_no = Column(Integer, index=False, default=1)
    question_statement = Column(String, index=False)
    topic = Column(String, index=True)

    def to_question(self) -> Question:
        return Question(
            question_id=int(self.question_id),
            part_no=int(self.part_no),
            question_statement=self.question_statement,
            topic=self.topic,
        )

