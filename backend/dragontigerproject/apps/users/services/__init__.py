from fastapi import APIRouter
from backend.dragontigerproject.apps.users.services.router.views import router as user_router

router = APIRouter()
router.include_router(user_router)
