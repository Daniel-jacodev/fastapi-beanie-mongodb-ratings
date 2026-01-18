from fastapi import APIRouter, HTTPException
from app.models.utilizador import Utilizador, UtilizadorCreate, UtilizadorUpdate
from typing import List
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. Criar
@router.post("/", response_model=Utilizador)
async def criar_utilizador(utilizador_in: UtilizadorCreate):
 
    novo_utilizador = Utilizador(
        nome=utilizador_in.nome,
        email=utilizador_in.email,
        senha=utilizador_in.senha
    )
    await novo_utilizador.insert()
    return novo_utilizador



# 2. Listar todos
@router.get("/", response_model=Page[Utilizador])
async def listar_utilizadores():
    return await apaginate(Utilizador.find())

# 3. Buscar por ID
@router.get("/{id}", response_model=Utilizador)
async def obter_utilizador(id: PydanticObjectId):
    try:
        return await apaginate(Utilizador.find(Utilizador.id == id))
    except Exception as e:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

# 4. Apagar
@router.delete("/{id}")
async def deletar_utilizador(id: PydanticObjectId):
    utilizador = await Utilizador.get(id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    await utilizador.delete()
    return {"message": "Utilizador removido com sucesso"}

# 5. Atualizar (Update usando o esquema UtilizadorUpdate)
@router.put("/{id}", response_model=Utilizador)
async def atualizar_utilizador(id: PydanticObjectId, dados_novos: UtilizadorUpdate):
    utilizador = await Utilizador.get(id)
    
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    if dados_novos.nome is not None:
        utilizador.nome = dados_novos.nome
    if dados_novos.email is not None:
        utilizador.email = dados_novos.email
    if dados_novos.senha is not None:
        utilizador.senha = dados_novos.senha
        
    await utilizador.save()
    return utilizador