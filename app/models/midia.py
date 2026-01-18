from typing import List, Optional
from beanie import Document, Link, PydanticObjectId
from .genero import Genero
from pydantic import BaseModel


class MidiaBase(BaseModel):
    titulo: str
    tipo: str
    ano: int
    sinopse: Optional[str] = None

class MidiaCreate(MidiaBase):
    generos_ids: List[PydanticObjectId] = []


class Midia(Document, MidiaBase):
    generos: List[Link[Genero]] = []

    class Settings:
        name = "midias"

class MidiaUpdate(BaseModel):
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    ano: Optional[int] = None
    sinopse: Optional[str] = None
    generos_ids: Optional[List[PydanticObjectId]] = None