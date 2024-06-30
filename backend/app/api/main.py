from fastapi import APIRouter

from app.api.routes import items, login, users, utils, registration, record

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(record.router, prefix='/record', tags=["record"])
api_router.include_router(registration.router, tags=["registration"], deprecated=True)
api_router.include_router(utils.router, prefix="/utils", tags=["utils"], deprecated=True)
api_router.include_router(items.router, prefix="/items", tags=["items"], deprecated=True)
