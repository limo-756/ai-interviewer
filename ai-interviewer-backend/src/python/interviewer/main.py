from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from interviewer.app.api.dao import user_dao
from . import database
from .app.api.dao.assessment_item_dao import AssessmentItemDao
from .app.api.dao.interview_dao import InterviewDao
from .app.api.dao.question_dao import QuestionsDao
from .app.api.external.LLMService import LLMService
from .app.api.requests.GetInterviewQuestionsRequest import GetInterviewQuestionsRequest
from .app.api.requests.LoginRequest import LoginRequest
from .app.api.requests.SignupRequest import SignupRequest
from .app.api.requests.StartInterviewRequest import StartInterviewRequest
from .app.api.requests.SubmitAnswerRequest import SubmitAnswerRequest
from .app.api.responses.EmptyResponse import EmptyResponse
from .app.api.responses.GetInterviewQuestionsResponse import GetInterviewQuestionsResponse
from .app.api.responses.GetInterviewReportResponse import GetInterviewReportResponse
from .app.api.responses.StartInterviewResponse import StartInterviewResponse
from .app.api.schemas.InterviewState import InterviewState
from .app.api.services.EvaluationManager import EvaluationManager
from .app.api.services.QuestionsManager import QuestionsManager
from .app.api.services.auth import Authenticator
from .app.api.utils.hash_utils import stable_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Application starting")

    # Create database tables on startup
    database.init_db()
    db = database.get_db()
    app.state.db = db
    app.state.interview_dao = InterviewDao(db)
    app.state.assessment_item_dao = AssessmentItemDao(db)
    app.state.questions_dao = QuestionsDao(db)
    app.state.llm_service = LLMService()
    app.state.evaluation_manager = EvaluationManager(app.state.interview_dao,
                                                     app.state.assessment_item_dao,
                                                     app.state.llm_service)
    app.state.questions_manager = QuestionsManager(app.state.questions_dao,
                                                   app.state.assessment_item_dao)
    print("Application started")

    yield  # The application will now handle requests

    # Shutdown logic
    print("Application shutdown: Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

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

def get_db_session() -> Session:
    return app.state.db

def get_interview_dao() -> InterviewDao:
    return app.state.interview_dao

def get_assessment_item_dao() -> AssessmentItemDao:
    return app.state.assessment_item_dao

def get_questions_dao() -> QuestionsDao:
    return app.state.questions_dao

def get_evaluation_manager() -> EvaluationManager:
    return app.state.evaluation_manager

def get_llm_service() -> LLMService:
    return app.state.llm_service

def get_questions_manager() -> QuestionsManager:
    return app.state.questions_manager



@app.get("/")
def read_root():
    return ({"message": "Hello, FastAPI!"})


@app.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db_session)):
    print(f"Request aa rahi hai for email: {req.email}")
    user = user_dao.get_user_by_email(db, req.email)

    if user is None or user.password != stable_hash(req.password):
        print(f"Type for the user is {type(user)}, {user.password}, {stable_hash(req.password)}, {req.password}")
        raise HTTPException(status_code=404, detail="User not found")

    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/signup")
async def signup(req: SignupRequest, db: Session = Depends(get_db_session)):
    print(f"Signup request for email: {req.email}")
    user = user_dao.create_user(db, req.name, req.email, req.password)
    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/start-interview")
async def start_interview(req: StartInterviewRequest, request: Request,
                          interview_dao: InterviewDao = Depends(get_interview_dao),
                          questions_manager: QuestionsManager = Depends(get_questions_manager)):
    print(f"Received access_token in header: {request.headers}")
    user_id = validate_user_and_get_userid(request)
    print(f"Starting interview for topic: {req.topic}")

    if req.resumeFile:
        print(f"Resume file provided (data URL starts with): {req.resumeFile[:70]}...")
    else:
        print("No resume file provided.")

    interview = interview_dao.create_interview(request.topic,
                                               user_id,
                                               req.number_of_questions,
                                               req.number_of_follow_up_questions,
                                               req.duration_in_mins)

    print(f"Interview created with ID: {interview.interview_id} for user {user_id}")
    questions_manager.assign_questions_for_interview(interview, req.number_of_questions)

    return StartInterviewResponse(
        interview_id=interview.interview_id,
        interviewer_name=interview.topic,
        total_questions=req.number_of_questions,
        number_of_follow_up_questions=req.number_of_follow_up_questions,
        total_duration_in_mins=req.duration_in_mins,
    )


@app.get("/get-interview-questions")
async def get_interview_questions(req: GetInterviewQuestionsRequest, request: Request,
                                  interview_dao: InterviewDao = Depends(get_interview_dao),
                                  assessment_item_dao: AssessmentItemDao = Depends(get_assessment_item_dao),
                                  questions_manager: QuestionsManager = Depends(get_questions_manager)) -> GetInterviewQuestionsResponse:
    user_id = validate_user_and_get_userid(request)
    interview = interview_dao.get_interview_by_id(req.interview_id)
    if req.all_questions:
        assessment_items = assessment_item_dao.get_all_part1_assessment_items_for_interview(req.interview_id)
    else:
        assessment_item = assessment_item_dao.get_assessment_item_by_interview_id_sequence_no_and_part_no(interview.interview_id,
                                                                                    req.question_no,
                                                                                    req.part_no)
        if assessment_item is None:
            assessment_item = questions_manager.generate_probing_question(interview, req.question_no)
        assessment_items = [assessment_item]

    questions = []
    for item in assessment_items:
        questions.append(GetInterviewQuestionsResponse.QuestionResponse(
            question_id=item.question_id,
            question_number=item.sequence_no,
            part_no=item.part_no,
            question_statement=item.question,
        ))

    return GetInterviewQuestionsResponse(questions)


@app.post("/submit-answer")
async def submit_answer(req: SubmitAnswerRequest, request: Request,
                        interview_dao: InterviewDao = Depends(get_interview_dao),
                        assessment_item_dao: AssessmentItemDao = Depends(get_assessment_item_dao)) -> EmptyResponse:
    user_id = validate_user_and_get_userid(request)
    interview = interview_dao.get_interview_by_id(req.interview_id)
    assessment_item = assessment_item_dao.get_assessment_item_by_interview_id_sequence_no_and_part_no(interview.interview_id,
                                                                                                      req.question_no,
                                                                                                      req.part_no)
    assessment_item_dao.update_assessment_item_with_answer(assessment_item.item_id, req.answer)
    return EmptyResponse()

@app.get("/get-interview-report")
async def get_interview_report(req: GetInterviewQuestionsRequest, request: Request,
                        interview_dao: InterviewDao = Depends(get_interview_dao),
                        assessment_item_dao: AssessmentItemDao = Depends(get_assessment_item_dao)) -> GetInterviewReportResponse:
    user_id = validate_user_and_get_userid(request)
    interview = interview_dao.get_interview_by_id(req.interview_id)
    if InterviewState.EVALUATED != interview.state:
        return GetInterviewReportResponse(0, 0, interview.state.value, [])

    assessment_items = assessment_item_dao.get_all_assessment_items_for_interview(req.interview_id)
    report = []
    total_score = 0
    total_marks = 0
    for item in assessment_items:
        report.append(GetInterviewReportResponse.InterviewReport(
            question_number=item.sequence_no,
            part_no=item.part_no,
            question_statement=item.question,
            answer=item.answer,
            evaluation_logs=item.evaluation_log,
            score=item.score,
            max_score=5,
        ))
        total_score += item.score
        total_marks += 5
    return GetInterviewReportResponse(
        total_score=total_score,
        total_marks=total_marks,
        status=interview.state.value,
        report=report,
    )


def validate_user_and_get_userid(request: Request) -> int:
    try:
        user_id = Authenticator().validate_token_and_get_user_id(request.headers['access_token'])
    except JWTError:
        raise HTTPException(status_code=400, detail="Session Expired")
    return user_id
