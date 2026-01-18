from beanie import Document, Link, PydanticObjectId
from .genero import Genero
from pydantic import BaseModel, ConfigDict

class MidiaBase(BaseModel):
    titulo: str
    tipo: str
    ano: int
    sinopse: str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class MidiaCreate(MidiaBase):
    generos_ids: list[PydanticObjectId] = []

class Midia(Document):
    titulo: str
    tipo: str
    ano: int
    sinopse: str | None = None
    generos: list[Link[Genero]] = []

    class Settings:
        name = "midias"

class MidiaUpdate(BaseModel):
    titulo: str | None = None
    tipo: str | None = None
    ano: int | None = None
    sinopse: str | None = None
    generos_ids: list[PydanticObjectId] | None = None