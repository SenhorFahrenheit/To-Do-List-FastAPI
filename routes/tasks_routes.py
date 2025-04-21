from fastapi import APIRouter
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/sign_up")
def sign_up(user: User):
    pass