from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password: str

    def __init__(self, user_id: int, name: str, email: str, password: str):
        super().__init__(user_id=user_id, name=name, email=email, password=password)
