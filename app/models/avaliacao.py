from datetime import datetime
from typing import Optional
from beanie import Document, Link, PydanticObjectId
from .utilizador import Utilizador
from .midia import Midia
from pydantic import BaseModel, Field


class AvalicaoCreate(BaseModel):

    utilizador_id: PydanticObjectId
    midia_id: PydanticObjectId
    pontuacao: int = Field(ge=1, le=10) 
    comentario: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "utilizador_id": "65a...",
                "midia_id": "65b...",
                "pontuacao": 10,
                "comentario": "Incrível! Recomendo muito."
            }
        }
    }

class AvalicaoUpdate(BaseModel):

    midia_id: PydanticObjectId
    pontuacao: int = Field(ge=1, le=10)
    comentario: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "midia_id": "65b...",
                "pontuacao": 10,
                "comentario": "Incrível! Recomendo muito."
            }
        }
    }
class Avaliacao(Document):
    utilizador: Link[Utilizador]
    midia: Link[Midia]
    pontuacao: int
    comentario: str
    data_avaliacao: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "avaliacoes"