from fastapi import APIRouter

from app.api.v1.endpoints import auth
from app.api.v1.endpoints import documents
from app.api.v1.endpoints import chat
from app.api.v1.endpoints import sessions
from app.api.v1.endpoints import history
from app.api.v1.endpoints import admin

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(chat.router)
api_router.include_router(sessions.router)
api_router.include_router(history.router)
api_router.include_router(admin.router)