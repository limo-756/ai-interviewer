# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Allow CORS from frontend
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",  # Alternate local address
    # Add any other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # allow specific origins
    allow_credentials=True,
    allow_methods=["*"],                # allow all HTTP methods
    allow_headers=["*"],                # allow all headers
)

@app.get("/")
def read_root():
    print("Request aa rahi hai")
    return ({"message": "Hello, FastAPI!"})

@app.post("/login")
def login():
    print("Request aa rahi hai")
    return {"message": "Succesful login"}
