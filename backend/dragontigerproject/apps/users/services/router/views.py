from fastapi.security import OAuth2PasswordRequestForm

from backend.dragontigerproject import User, Game, Round, Stats
from backend.dragontigerproject.apps.users.services.auth.auth import get_password_hash, authenticate_user, \
    create_access_token
from backend.dragontigerproject.apps.users.services.models.models import Token
from fastapi import APIRouter, HTTPException, Depends, status
from backend.dragontigerproject.config import settings
from datetime import timedelta


router = APIRouter(prefix="")


@router.post("/signup")
async def signup(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    await user_data.save()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("create/game", status_code=201, response_model=Game)
async def create_game(item: Game):
    return await item.save()


@router.get("get/all/game")
async def get_all():
    return await Game.find_all().to_list()


@router.delete("delete/all/game")
async def delete_all():
    return await Game.delete_all()


@router.post("create/round", status_code=201)
async def get_all(item: Round):
    return await item.save()


@router.get("get/all/round")
async def get_all():
    return await Round.find_all().to_list()


@router.delete("delete/all/round")
async def delete_all():
    return await Round.delete_all()


@router.get("get/all/stats")
async def get_all():
    return await Stats.find_all().to_list()


@router.delete("delete/all/stats")
async def delete_all():
    return await Stats.delete_all()
