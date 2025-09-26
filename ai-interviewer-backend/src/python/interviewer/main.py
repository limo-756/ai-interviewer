from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from interviewer.app.api.dao import user_dao
from . import database
from .app.api.dao.assessment_item_dao import AssessmentItemDao
from .app.api.dao.interview_dao import InterviewDao
from .app.api.requests.GetInterviewQuestionsRequest import GetInterviewQuestionsRequest
from .app.api.requests.LoginRequest import LoginRequest
from .app.api.requests.SignupRequest import SignupRequest
from .app.api.requests.StartInterviewRequest import StartInterviewRequest
from .app.api.responses.GetInterviewQuestionsResponse import GetInterviewQuestionsResponse
from .app.api.responses.StartInterviewResponse import StartInterviewResponse
from .app.api.services.auth import Authenticator
from .app.api.utils.hash_utils import stable_hash

# Create database tables on startup
database.init_db()

app = FastAPI()

# Allow CORS from frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)


# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_interview_dao(db: Annotated[Session, Depends(get_db)]):
    return InterviewDao(db)


def get_assessment_item_dao(db: Annotated[Session, Depends(get_db)]):
    return AssessmentItemDao(db)


@app.get("/")
def read_root():
    return ({"message": "Hello, FastAPI!"})


@app.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    print(f"Request aa rahi hai for email: {req.email}")
    user = user_dao.get_user_by_email(db, req.email)

    if user is None or user.password != stable_hash(req.password):
        print(f"Type for the user is {type(user)}, {user.password}, {stable_hash(req.password)}, {req.password}")
        raise HTTPException(status_code=404, detail="User not found")

    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/signup")
async def signup(req: SignupRequest, db: Session = Depends(get_db)):
    print(f"Signup request for email: {req.email}")
    user = user_dao.create_user(db, req.name, req.email, req.password)
    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/start-interview")
async def start_interview(req: StartInterviewRequest, request: Request,
                          interview_dao: InterviewDao = Depends(get_interview_dao)):
    print(f"Received access_token in header: {request.headers}")
    user_id = validate_user_and_get_userid(request)
    print(f"Starting interview for topic: {req.topic}")

    if req.resumeFile:
        print(f"Resume file provided (data URL starts with): {req.resumeFile[:70]}...")
    else:
        print("No resume file provided.")

    interview = interview_dao.create_interview(request.topic, user_id)


    print(f"Interview created with ID: {interview.interview_id} for user {user_id}")
    return StartInterviewResponse(
        interview_id=interview.interview_id,
        interviewer_name=interview.topic,
        total_questions=10,
        total_duration_in_mins=30,
    )


@app.get("/get-interview-questions")
async def get_interview_questions(req: GetInterviewQuestionsRequest, request: Request,
                                  interview_dao: InterviewDao = Depends(get_interview_dao),
                                  assessment_item_dao: AssessmentItemDao = Depends(get_assessment_item_dao)):
    user_id = validate_user_and_get_userid(request)
    interview = interview_dao.get_interview_by_id(req.interview_id)
    if req.all_questions:
        assessment_items = assessment_item_dao.get_all_assessment_items_for_interview(req.interview_id)
    else:
        assessment_items = [
            assessment_item_dao.get_assessment_item_by_interview_id_and_sequence_no(interview.interview_id,
                                                                                    req.question_no)]

    questions = []
    for item in assessment_items:
        questions.append(GetInterviewQuestionsResponse.QuestionResponse(
            question_id=item.question_id,
            question_number=item.sequence_no,
            question_statement=item.question,
        ))

    return GetInterviewQuestionsResponse(questions)


@app.post("/submit-answer")
async def submit_answer():
    return


def validate_user_and_get_userid(request: Request) -> int:
    try:
        user_id = Authenticator().validate_token_and_get_user_id(request.headers['access_token'])
    except JWTError:
        raise HTTPException(status_code=400, detail="Session Expired")
    return user_id
