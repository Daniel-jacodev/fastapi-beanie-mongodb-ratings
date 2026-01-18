from fastapi import APIRouter, HTTPException
from app.models.genero import Genero, GeneroCreate
from typing import List
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. CRIAR 
@router.post("/", response_model=Genero)
async def criar_genero(genero_in: GeneroCreate):
    novo_genero = Genero(
        nome=genero_in.nome
    )
    await novo_genero.insert()
    return novo_genero



# 2. LISTAR TODOS
@router.get("/", response_model=Page[Genero])
async def listar_generos():
    return await apaginate(Genero.find())

# 3. BUSCAR POR ID
@router.get("/{id}", response_model=Genero)
async def obter_genero(id: PydanticObjectId):
  try:
      return await apaginate(Genero.find(Genero.id == id))
  except Exception as e:
      raise HTTPException(status_code=404, detail="Gênero não encontrado")


# 4. APAGAR 
@router.delete("/{id}")
async def deletar_genero(id: PydanticObjectId):
    genero = await Genero.get(id)
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    await genero.delete()
    return {"message": "Gênero removido com sucesso"}

# 5. ATUALIZAR 
@router.put("/{id}", response_model=Genero)
async def atualizar_genero(id: PydanticObjectId, dados_novos: GeneroCreate) -> Genero:
    genero = await Genero.get(id)
    
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
  
    for key, value in dados_novos.dict().items():
        setattr(genero, key, value)

    await genero.save()
    return genero
