from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database.postgres.connection.postgres_connection import PostgresPool
from src.api.routes.auth_route import setup_auth_routes
from src.api.routes.chatters_routes import setup_chatters_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    PostgresPool.init_pool(minconn=1, maxconn=5)
    print("Conexão realizada ao banco (pool inicializado)")

    yield  # app executa aqui

    # Shutdown
    PostgresPool.close_all()
    print("Fechada todas conexões com o banco")


app = FastAPI(lifespan=lifespan)

# Rotas são registradas fora do lifespan porque não precisam da conexão diretamente
app.include_router(setup_auth_routes())
app.include_router(setup_chatters_routes())
