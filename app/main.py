from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routes import genero_routes, utilizador_rountes, midia_routes, avaliacao_routes
from app.core.database import init_db


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(genero_routes.router, prefix="/generos", tags=["Gêneros"])
app.include_router(utilizador_rountes.router, prefix="/utilizadores", tags=["Utilizadores"])
app.include_router(midia_routes.router, prefix="/midias", tags=["Mídias"])
app.include_router(avaliacao_routes.router, prefix="/avaliacoes", tags=["Avaliações"])

add_pagination(app)