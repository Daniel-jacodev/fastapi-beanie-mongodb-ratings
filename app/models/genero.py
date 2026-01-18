from beanie import Document
from pydantic import BaseModel

class GeneroBase(BaseModel):
    nome: str

class GeneroCreate(GeneroBase):
    pass

class Genero(Document, GeneroBase):
    class Settings:
        name = "generos"
