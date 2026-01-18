from fastapi import APIRouter, HTTPException, status
from app.models.genero import Genero, GeneroCreate
# Removido typing List (Feedback 8)
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. CRIAR
@router.post("/", response_model=Genero, status_code=status.HTTP_201_CREATED)
async def criar_genero(genero_in: GeneroCreate):
    existente = await Genero.find_one(Genero.nome == genero_in.nome)
    if existente:
        raise HTTPException(status_code=409, detail="Gênero já cadastrado")
        
    novo_genero = Genero(nome=genero_in.nome)
    await novo_genero.insert()
    return novo_genero

# 2. LISTAR TODOS
@router.get("/", response_model=Page[Genero])
async def listar_generos():
    return await apaginate(Genero.find().sort(+Genero.nome))

# 3. BUSCAR POR ID
@router.get("/{id}", response_model=Genero)
async def obter_genero(id: PydanticObjectId):
    genero = await Genero.get(id)
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    return genero

# 4. ATUALIZAR 
@router.put("/{id}", response_model=Genero)
async def atualizar_genero(id: PydanticObjectId, dados_novos: GeneroCreate):
    genero = await Genero.get(id)
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
 
    update_data = dados_novos.model_dump()
    for key, value in update_data.items():
        setattr(genero, key, value)

    await genero.save()
    return genero

# 5. APAGAR 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_genero(id: PydanticObjectId):
    genero = await Genero.get(id)
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    await genero.delete()
    return None