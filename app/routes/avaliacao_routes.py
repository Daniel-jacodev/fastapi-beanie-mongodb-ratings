from fastapi import APIRouter, HTTPException
from app.models.avaliacao import Avaliacao, AvaliacaoCreate, AvaliacaoUpdate # Corrigido typo
from app.models.utilizador import Utilizador
from app.models.midia import Midia
# removido typing List
from beanie import PydanticObjectId, Link
from pydantic import EmailStr
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

router = APIRouter()

# 1. Criar avaliação
@router.post("/", response_model=Avaliacao, status_code=201)
async def criar_avaliacao(avaliacao_in: AvaliacaoCreate):
    utilizador = await Utilizador.get(avaliacao_in.utilizador_id)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    
    midia = await Midia.get(avaliacao_in.midia_id)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")

    nova_avaliacao = Avaliacao(
        utilizador=Link(utilizador),
        midia=Link(midia),
        pontuacao=avaliacao_in.pontuacao,
        comentario=avaliacao_in.comentario
    )
    
    await nova_avaliacao.insert()
    return nova_avaliacao

# 2. Listar todos
@router.get("/", response_model=Page[Avaliacao])
async def listar_avaliacoes():
    return await apaginate(Avaliacao.find(fetch_links=True).sort(-Avaliacao.id))

# 3. Obter por ID
@router.get("/{avaliacao_id}", response_model=Avaliacao)
async def obter_avaliacao(avaliacao_id: PydanticObjectId):
    avaliacao = await Avaliacao.get(avaliacao_id, fetch_links=True)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao

# 4. Obter avaliações por utilizador
@router.get("/utilizador/{utilizador_email}", response_model=Page[Avaliacao])
async def obter_avaliacoes_por_utilizador(utilizador_email: EmailStr):
    utilizador = await Utilizador.find_one(Utilizador.email == utilizador_email)
    if not utilizador:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    return await apaginate(Avaliacao.find(
        Avaliacao.utilizador.id == utilizador.id,
        fetch_links=True
    ).sort(-Avaliacao.id))

# 5. Obter avaliações por mídia
@router.get("/midia/{midia_titulo}", response_model=Page[Avaliacao])
async def obter_avaliacoes_por_midia(midia_titulo: str):
    midia = await Midia.find_one(Midia.titulo == midia_titulo)
    if not midia:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")

    return await apaginate(Avaliacao.find(
        Avaliacao.midia.id == midia.id,
        fetch_links=True
    ).sort(-Avaliacao.id))

# 6. Atualizar
@router.put("/{avaliacao_id}", response_model=Avaliacao)
async def atualizar_avaliacao(avaliacao_id: PydanticObjectId, dados_novos: AvaliacaoUpdate):
    avaliacao = await Avaliacao.get(avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    avaliacao.pontuacao = dados_novos.pontuacao
    avaliacao.comentario = dados_novos.comentario

    await avaliacao.save()
    return avaliacao

# 7. Deletar
@router.delete("/{avaliacao_id}", status_code=204)
async def deletar_avaliacao(avaliacao_id: PydanticObjectId):
    avaliacao = await Avaliacao.get(avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    await avaliacao.delete()
    return None


# 8. Ranking por notas (Top 15)
@router.get("/ranking/top15", response_model=list[dict])
async def obter_top_15_ranking():
    pipeline = [
        {"$group": {"_id": "$midia.$id", "media_nota": {"$avg": "$pontuacao"}, "total_avaliacoes": {"$sum": 1}}},
        {"$sort": {"media_nota": -1}},
        {"$limit": 15}
    ]
    
    colecao = Avaliacao.get_pymongo_collection()
    cursor = colecao.aggregate(pipeline)
    
    resultados = []
    async for doc in cursor:
        midia = await Midia.get(doc["_id"])
        if midia:
            resultados.append({
                "titulo": midia.titulo,
                "media_nota": round(doc["media_nota"], 1),
                "total_avaliacoes": doc["total_avaliacoes"]
            })
            
    return resultados