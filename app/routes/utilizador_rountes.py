from fastapi import APIRouter, HTTPException, status
from app.models.utilizador import Utilizador, UtilizadorCreate, UtilizadorUpdate
# Removido typing List (Feedback 8)
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. Criar
@router.post("/", response_model=Utilizador, status_code=status.HTTP_201_CREATED)
async def criar_utilizador(utilizador_in: UtilizadorCreate):
    existente = await Utilizador.find_one(Utilizador.email == utilizador_in.email)
    if existente:
        raise HTTPException(status_code=409, detail="Email já registado")

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
    return await apaginate(Utilizador.find().sort(+Utilizador.nome))

# 3. Buscar por ID
@router.get("/{id}", response_model=Utilizador)
async def obter_utilizador(id: PydanticObjectId):
    utilizador = await Utilizador.get(id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return utilizador

# 4. Atualizar
@router.put("/{id}", response_model=Utilizador)
async def atualizar_utilizador(id: PydanticObjectId, dados_novos: UtilizadorUpdate):
    utilizador = await Utilizador.get(id)
    
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    update_data = dados_novos.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(utilizador, key, value)
        
    await utilizador.save()
    return utilizador

# 5. Apagar
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_utilizador(id: PydanticObjectId):
    utilizador = await Utilizador.get(id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    await utilizador.delete()
    return None