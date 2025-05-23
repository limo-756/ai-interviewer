# main.py
from fastapi import FastAPI, Header, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError
from sqlalchemy.orm import Session
import uuid

from . import crud, database
from .app.api.services.auth import Authenticator

# Create database tables on startup
database.init_db()

app = FastAPI()


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class StartInterviewRequest(BaseModel):
    topic: str
    resumeFile: str


# Allow CORS from frontend
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",  # Alternate local address
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow specific origins
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


@app.get("/")
def read_root():
    return ({"message": "Hello, FastAPI!"})


@app.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    print(f"Request aa rahi hai for email: {req.email}")
    user = crud.get_user_by_email(db, req.email)
    if user is None or user.password != hash(req.password):
        print(f"Type for the user is {type(user)}, {user.password}, {hash(req.password)}, {req.password}")
        raise HTTPException(status_code=404, detail="User not found")

    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/signup")
async def signup(req: SignupRequest, db: Session = Depends(get_db)):
    print(f"Signup request for email: {req.email}")
    user = crud.create_user(db, req.name, req.email, req.password)
    access_token = Authenticator().create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/start-interview")
async def start_interview(request: Request):
    print(f"Received access_token in header: {request.headers}")

    try:
        user_id = Authenticator().validate_token_and_get_user_id(request.headers['access_token'])
    except JWTError:
        raise HTTPException(status_code=400, detail="Session Expired")
    print(f"Validated user_id: {user_id}")

    req = request.data
    print(f"Starting interview for topic: {req.topic}")

    if req.resumeFile:
        # Assuming resumeFile is a base64 data URL. Just printing a snippet for confirmation.
        print(f"Resume file provided (data URL starts with): {req.resumeFile[:70]}...")
        # Add actual resume processing logic here (e.g., decode, save, parse)
    else:
        print("No resume file provided.")
    
    # Simulate interview creation and return a more dynamic ID
    # In a real application, you would create an interview record in the database.
    interview_id = str(uuid.uuid4()) # Generate a unique ID for the interview
    
    print(f"Interview created with ID: {interview_id} for user {user_id}")
    return {"interview_id": interview_id}


# @app.post("/items/", response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return crud.create_item(db=db, item=item)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
#
#
# @app.get("/items/{item_id}", response_model=schemas.Item)
# def read_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = crud.get_item(db, item_id=item_id)
#     if db_item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return db_item
