import asyncio
import os
import random
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from app.models.genero import Genero
from app.models.utilizador import Utilizador
from app.models.midia import Midia
from app.models.avaliacao import Avaliacao

load_dotenv()

async def popular():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db_name = os.getenv("DATABASE_NAME")
    
    print(f"🔗 Conectando ao banco: {db_name}...")
    await init_beanie(
        database=client[db_name],
        document_models=[Genero, Utilizador, Midia, Avaliacao]
    )

    print("🧹 Limpando dados antigos...")
    await Avaliacao.find_all().delete()
    await Midia.find_all().delete()
    await Utilizador.find_all().delete()
    await Genero.find_all().delete()

    print("🎭 Inserindo Gêneros...")
    g_anime = await Genero(nome="Anime").insert()
    g_ficcao = await Genero(nome="Ficção Científica").insert()
    g_acao = await Genero(nome="Ação").insert()
    g_drama = await Genero(nome="Drama").insert()
    generos_lista = [g_anime, g_ficcao, g_acao, g_drama]

    print("👤 Inserindo Utilizadores...")
    usuarios = []
    for i in range(1, 6):
        u = await Utilizador(nome=f"Usuario_{i}", email=f"user{i}@teste.com").insert()
        usuarios.append(u)

    print("📺 Inserindo 21 Mídias e Avaliações...")
    dados_midias = [
        ("Cavaleiros do Zodíaco", "Desenho", 1994, [g_anime]),
        ("Inception", "Filme", 2010, [g_ficcao, g_acao]),
        ("Matrix", "Filme", 1999, [g_ficcao]),
        ("Interstellar", "Filme", 2014, [g_ficcao, g_drama]),
        ("Dragon Ball Z", "Desenho", 1989, [g_anime, g_acao]),
        ("Naruto", "Desenho", 2002, [g_anime]),
        ("One Piece", "Desenho", 1999, [g_anime]),
        ("The Batman", "Filme", 2022, [g_acao, g_drama]),
        ("Blade Runner 2049", "Filme", 2017, [g_ficcao]),
        ("Akira", "Filme", 1988, [g_anime, g_ficcao]),
        ("Duna", "Filme", 2021, [g_ficcao]),
        ("Gladiador", "Filme", 2000, [g_acao, g_drama]),
        ("Your Name", "Filme", 2016, [g_anime, g_drama]),
        ("O Exterminador do Futuro", "Filme", 1984, [g_acao, g_ficcao]),
        ("Attack on Titan", "Desenho", 2013, [g_anime, g_drama]),
        ("O Resgate do Soldado Ryan", "Filme", 1998, [g_acao, g_drama]),
        ("Cowboy Bebop", "Desenho", 1998, [g_anime, g_ficcao]),
        ("Parasita", "Filme", 2019, [g_drama]),
        ("Dunkirk", "Filme", 2017, [g_acao, g_drama]),
        ("Vingadores: Ultimato", "Filme", 2019, [g_acao, g_ficcao]),
        ("Spider-Man: No Way Home", "Filme", 2021, [g_acao, g_ficcao])
    ]

    for titulo, tipo, ano, gens in dados_midias:
        # 1. Inserir Mídia
        m = await Midia(
            titulo=titulo,
            tipo=tipo,
            ano=ano,
            sinopse=f"Uma obra incrível do gênero {tipo}.",
            generos=gens
        ).insert()

        # 2. Criar 2 avaliações aleatórias para cada mídia para testar a média
        for _ in range(2):
            await Avaliacao(
                utilizador=random.choice(usuarios),
                midia=m,
                pontuacao=random.randint(7, 10), # Notas entre 7 e 10
                comentario="Gostei muito, recomendo!"
            ).insert()

    print(f"\n✅ Sucesso!")
    print(f"📊 Foram criados:")
    print(f"- {len(generos_lista)} Gêneros")
    print(f"- {len(usuarios)} Utilizadores")
    print(f"- {len(dados_midias)} Mídias")
    print(f"- {len(dados_midias) * 2} Avaliações")

if __name__ == "__main__":
    asyncio.run(popular())