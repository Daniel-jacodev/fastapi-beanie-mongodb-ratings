from beanie import Document
from pydantic import BaseModel, EmailStr

class UtilizadorBase(BaseModel):
    nome: str
    email: EmailStr


class UtilizadorCreate(UtilizadorBase):
    pass

class Utilizador(Document, UtilizadorBase):
    class Settings:
        name = "utilizadores"

class UtilizadorUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None