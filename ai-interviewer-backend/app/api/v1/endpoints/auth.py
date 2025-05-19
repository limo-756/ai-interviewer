from fastapi import APIRouter

router = APIRouter()

@router.post("/signup")
async def signup():
    # Signup logic here
    return {"message": "Signup successful"}

@router.post("/login")
async def login():
    # Login logic here
    return {"message": "Login successful"} 