from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

    def __init__(self, name: str, email: str, password: str):
        super().__init__(name=name, email=email, password=password)
