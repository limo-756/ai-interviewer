import json
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from interviewer.app.api.dao.assessment_item_dao import AssessmentItemDao
from interviewer.app.api.dao.interview_dao import InterviewDao
from interviewer.app.api.dao.question_dao import QuestionsDao

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get DB session
def get_db():
    try:
        yield SessionLocal
    finally:
        SessionLocal.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    populate_questions_table()


def populate_questions_table(questions_dao: QuestionsDao = Depends(get_questions_dao)):
    with open("ai-interviewer-backend/questionBank.json", 'r') as f:
        questions = json.load(f)

    for question in questions:
        questions_dao.create_question(
            topic=question['topic'],
            question=question['question'],
            question_id=question['question_id'])
