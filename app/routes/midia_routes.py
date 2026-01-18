from fastapi import APIRouter, HTTPException
from app.models.midia import Midia, MidiaCreate, MidiaUpdate
from app.models.genero import Genero
from typing import List
from beanie import PydanticObjectId, Link
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
import re

router = APIRouter()

# 1. Criar
@router.post("/", response_model=Midia)
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
    return await apaginate(Midia.find())


# 3. Obter midia por titulo
@router.get("/busca/{termo}", response_model=Page[Midia])
async def obter_midias_por_titulo(termo: str):
    filtro = {"titulo": {"$regex": termo, "$options": "i"}}
    return await apaginate(Midia.find(filtro))

# 4. Obter por ID
@router.get("/{midia_id}", response_model=Midia)
async def obter_midia(midia_id: PydanticObjectId):
    try:
        return await Midia.find(Midia.id == midia_id).to_list()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")

# 5. Obter por nome do género
@router.get("/genero-nome/{nome_genero}", response_model=Page[Midia])
async def obter_midias_por_nome_genero(nome_genero: str):
    genero = await Genero.find_one({"nome": {"$regex": nome_genero, "$options": "i"}})
    
    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    return await apaginate(Midia.find(
        Midia.generos.id == genero.id,
        fetch_links=True
    ))
    

# 5. Atualizar
@router.put("/{midia_id}", response_model=Midia)
async def atualizar_midia(midia_id: PydanticObjectId, dados_novos: MidiaUpdate):
    midia = await Midia.get(midia_id)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")
    
    if dados_novos.titulo: midia.titulo = dados_novos.titulo
    if dados_novos.tipo: midia.tipo = dados_novos.tipo
    if dados_novos.ano: midia.ano = dados_novos.ano
    if dados_novos.sinopse: midia.sinopse = dados_novos.sinopse
    
    if dados_novos.generos_ids is not None:
        nova_lista_links = []
        for gid in dados_novos.generos_ids:
            g = await Genero.get(gid)
            if g:
                nova_lista_links.append(Link(g))
        midia.generos = nova_lista_links
    
    await midia.save()
    return midia

# 6. Deletar
@router.delete("/{midia_id}")
async def deletar_midia(midia_id: PydanticObjectId):
    midia = await Midia.get(midia_id)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")
    await midia.delete()
    return {"message": "Mídia removida com sucesso"}