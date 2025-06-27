from fastapi import APIRouter, FastAPI
import nonebot

from .config import WEB_PREFIX
from .plugins.ww_login.router import router as ww_login_router

app: FastAPI = nonebot.get_app()


router = APIRouter(prefix=WEB_PREFIX)

router.include_router(ww_login_router)

app.include_router(router)
