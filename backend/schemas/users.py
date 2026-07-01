from pydantic import BaseModel
from backend.models.user import Role

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    secteur_activite: str | None = None
    role: Role 

class UserLogin(BaseModel):
    email: str
    password: str

    