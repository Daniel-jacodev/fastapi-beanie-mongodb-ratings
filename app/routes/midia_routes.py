from fastapi import APIRouter, HTTPException, status
from app.models.midia import Midia, MidiaCreate, MidiaUpdate
from app.models.genero import Genero
# Removido typing List (Feedback 8)
from beanie import PydanticObjectId, Link
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. Criar
@router.post("/", response_model=Midia, status_code=status.HTTP_201_CREATED)
async def criar_midia(midia_in: MidiaCreate):
    generos_encontrados = []
    for gid in midia_in.generos_ids:
        genero = await Genero.get(gid)
        if not genero:
            raise HTTPException(status_code=404, detail=f"Gênero {gid} não encontrado")
        generos_encontrados.append(genero)
    
    nova_midia = Midia(
        **midia_in.model_dump(exclude={"generos_ids"}), 
        generos=generos_encontrados 
    )
    
    await nova_midia.insert()
    return nova_midia

# 2. Listar todos
@router.get("/", response_model=Page[Midia])
async def listar_midias():
    return await apaginate(Midia.find(fetch_links=True).sort(+Midia.titulo))

# 2.1 Listar todos por ano 
@router.get("/ano/{ano}", response_model=Page[Midia])
async def listar_por_ano(ano: int):
    return await apaginate(Midia.find(Midia.ano == ano, fetch_links=True).sort(+Midia.titulo))

# 3. Obter midia por titulo (Busca Parcial
@router.get("/busca/{termo}", response_model=Page[Midia])
async def obter_midias_por_titulo(termo: str):
    filtro = {"titulo": {"$regex": termo, "$options": "i"}}
    return await apaginate(Midia.find(filtro, fetch_links=True).sort(+Midia.titulo))

# 4. Obter por ID
@router.get("/{midia_id}", response_model=Midia)
async def obter_midia(midia_id: PydanticObjectId):
    midia = await Midia.get(midia_id, fetch_links=True)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")
    return midia

# 5. Obter por nome do genero
@router.get("/genero-nome/{nome_genero}", response_model=Page[Midia])
async def obter_midias_por_nome_genero(nome_genero: str):
    genero = await Genero.find_one({"nome": {"$regex": nome_genero, "$options": "i"}})
    
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    
    return await apaginate(Midia.find(
        Midia.generos.id == genero.id,
        fetch_links=True
    ).sort(+Midia.titulo))

# 5. Atualizar
@router.put("/{midia_id}", response_model=Midia)
async def atualizar_midia(midia_id: PydanticObjectId, dados_novos: MidiaUpdate):
    midia = await Midia.get(midia_id)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")
    
    update_data = dados_novos.model_dump(exclude_unset=True)
    
    if "generos_ids" in update_data:
        novos_generos = []
        for gid in update_data["generos_ids"]:
            g = await Genero.get(gid)
            if g:
                novos_generos.append(g)
        midia.generos = novos_generos
        del update_data["generos_ids"]

    for key, value in update_data.items():
        setattr(midia, key, value)
    
    await midia.save()
    return await Midia.get(midia_id, fetch_links=True)

# 6. Deletar
@router.delete("/{midia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_midia(midia_id: PydanticObjectId):
    midia = await Midia.get(midia_id)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")
    await midia.delete()
    return None