from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from nonebot.compat import model_dump
from pydantic import BaseModel

from ...waves_api.config import MAIN_URL
from .data_source import LoginManager, cache

TEMPLATE_PATH = Path(__file__).parent / "templates"
# 创建Jinja2模板环境
waves_templates = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

router = APIRouter(prefix="/login")


class LoginModel(BaseModel):
    auth: str
    """登录凭证"""
    mobile: str
    """手机号"""
    code: str
    """验证码"""


@router.get("/{token}")
async def _(token: str):
    temp = cache.get(token)
    if temp is None:
        template = waves_templates.get_template("404.html")
        return HTMLResponse(template.render())
    else:
        url = await LoginManager.get_login_url()
        template = waves_templates.get_template("index.html")
        return HTMLResponse(
            template.render(
                submit_url=f"{url}/zhenxun/waves/login/go",
                auth=token,
                user_id=temp.get("user_id", ""),
                kuro_url=MAIN_URL,
                year=datetime.now().year,
            )
        )


@router.post("/go")
async def waves_login(data: LoginModel):
    temp = cache.get(data.auth)
    if temp is None:
        return {"success": False, "msg": "登录超时"}

    temp.update(model_dump(data))
    cache.set(data.auth, temp)
    return {"success": True}
