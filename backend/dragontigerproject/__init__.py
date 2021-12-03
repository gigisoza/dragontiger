import motor.motor_asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from beanie import init_beanie

from .apps.users.services.server.server import sio_app, sio
from .config import settings
from backend.dragontigerproject.apps.users.services import router
from backend.dragontigerproject.apps.users.services.docs.documents import User, Game, Round, Stats


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)
    app.mount("/ws", sio_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup_event():
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(database=client[settings.MONGODB_DATABASE_NAME], document_models=[User, Game, Round, Stats])

    return app
