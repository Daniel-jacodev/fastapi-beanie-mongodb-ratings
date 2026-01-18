from beanie import Document, Link
from pydantic import BaseModel
from app.models.utilizador import Utilizador
from app.models.midia import Midia
from beanie import PydanticObjectId


class Avaliacao(Document):
    utilizador: Link[Utilizador]
    midia: Link[Midia]
    pontuacao: int
    comentario: str | None = None

    class Settings:
        name = "avaliacoes"

class AvaliacaoCreate(BaseModel):
    utilizador_id: PydanticObjectId
    midia_id: PydanticObjectId
    pontuacao: int
    comentario: str | None = None


class AvaliacaoUpdate(BaseModel):
    pontuacao: int
    comentario: str | None = None