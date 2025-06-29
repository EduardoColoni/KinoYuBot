from fastapi import FastAPI
from src.api.routes.auth_route import router as auth_router
from src.api.routes.chatters_routes import router as chatters_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chatters_router)