# main.py
from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import schemas
from app import crud
from app import database

# JWT Configuration
SECRET_KEY = "your-secret-key"  # Change this in a real application!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 40

# Create database tables on startup
database.init_db()

app = FastAPI()


# Define a Pydantic model for the request body
class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


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


# Helper function to create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/")
def read_root():
    print("Request aa rahi hai")
    return ({"message": "Hello, FastAPI!"})


@app.post("/login")
async def login(req: LoginRequest, headers: str | None = Header(default=None), db: Session = Depends(get_db)):
    print(f"Request aa rahi hai for email: {req.email}")
    print(f"User-Agent: {headers}")
    user = crud.get_user_by_email(db, req.email)
    if user is None or user.password != hash(req.password):
        raise HTTPException(status_code=404, detail="User not found")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": req.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


@app.post("/signup")
async def signup(req: SignupRequest, db: Session = Depends(get_db)):
    print(f"Signup request for email: {req.email}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": req.email}, expires_delta=access_token_expires
    )

    user = schemas.User(req.name, req.email, req.password)
    crud.create_user(db=db, user=user)
    print("Entry successful")
    return {"access_token": access_token, "token_type": "bearer", "message": "Login is successful"}


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
