from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: int

    def __init__(self, id: int, name: str, email: str, password: int):
        super().__init__(id=id, name=name, email=email, password=password)
