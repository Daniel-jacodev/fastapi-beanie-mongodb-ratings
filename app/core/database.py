from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.utilizador import Utilizador
from app.models.midia import Midia
from app.models.genero import Genero
from app.models.avaliacao import Avaliacao
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    # 1. Criar o cliente do MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    
    # 2. Inicializar o Beanie com a lista de modelos
    await init_beanie(
        database=client[os.getenv("DATABASE_NAME")],
        document_models=[
            Utilizador,
            Midia,
            Genero,
            Avaliacao
        ]
    )
