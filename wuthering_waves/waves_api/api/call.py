from typing import Any

from httpx import Response
from nonebot.compat import model_dump
import ujson as json

from zhenxun.services.log import logger
from zhenxun.utils.decorator.retry import Retry
from zhenxun.utils.http_utils import AsyncHttpx

from ...base_models import WwBaseResponse
from ...config import LOG_COMMAND
from ...exceptions import APIResponseException
from ..captcha import get_solver
from ..captcha.base import CaptchaResult
from ..captcha.errors import CaptchaError
from ..const import (
    GAME_ID,
    NET_SERVER_ID_MAP,
    SERVER_ID,
    SERVER_ID_NET,
)
from ..error_code import (
    WAVES_CODE_999,
)
from ..headers import get_headers
from ..models import CallResult


def login_platform() -> str:
    """登录平台

    返回:
        str: 登录平台
    """
    return "ios"


if captcha_solver := get_solver():
    logger.info(f"验证码识别器初始化成功: {captcha_solver.get_name()}", LOG_COMMAND)


def get_server_id(role_id: str) -> str:
    if int(role_id) >= 200000000:
        return NET_SERVER_ID_MAP.get(int(role_id) // 100000000, SERVER_ID_NET)
    return SERVER_ID


async def solve_captcha(
    url: str, max_retries: int = 3
) -> CallResult | CaptchaResult | dict[str, Any]:
    """破解验证码"""
    if not captcha_solver:
        return CallResult(
            code=WAVES_CODE_999,
            data="验证码识别器未初始化",
            is_success=False,
        )
    for _ in range(max_retries):
        try:
            return await captcha_solver.solve()
        except CaptchaError as e:
            logger.warning(
                f"url:[{url}] 验证码破解失败，正在重试 {_ + 1} 次", LOG_COMMAND, e=e
            )

    return CallResult(
        code=WAVES_CODE_999,
        data="验证码破解失败",
        is_success=False,
    )


class CallApi:
    @classmethod
    def __format_data(cls, response: Response) -> WwBaseResponse:
        """格式化响应数据"""
        try:
            json_data = response.json()
        except Exception as e:
            logger.warning(f"解析响应数据失败: {response.text}", LOG_COMMAND, e=e)
            json_data = json.loads(response.text)
        if "data" not in json_data:
            json_data["data"] = None
        if "success" not in json_data:
            # 有些请求没有success字段
            json_data["success"] = True
        try:
            raw_data = WwBaseResponse(url=str(response.url), **json_data)
        except APIResponseException:
            raise
        except Exception as e:
            logger.warning(
                f"WwBaseResponse实例化失败: {response.text}", LOG_COMMAND, e=e
            )
            raw_data = WwBaseResponse(
                url=str(response.url),
                code=WAVES_CODE_999,
                data=response.text,
                msg=response.text,
                success=False,
            )
        try:
            if isinstance(raw_data.data, str):
                raw_data.data = json.loads(raw_data.data)
        except Exception as e:
            logger.warning(
                f"raw_data.data 转化json解析响应数据失败: {response.text}",
                LOG_COMMAND,
                e=e,
            )
        return raw_data

    @classmethod
    def default_params(cls, role_id: str, server_id: str | None) -> dict:
        """默认参数"""
        return {
            "gameId": GAME_ID,
            "serverId": server_id or get_server_id(role_id),
            "roleId": role_id,
        }

    @classmethod
    @Retry.api()
    async def call_post(
        cls, url: str, header: dict | None = None, **kwargs
    ) -> WwBaseResponse:
        """调用POST请求"""
        if not header:
            header = await get_headers()
        if header:
            header.pop("roleId", None)
        response = await AsyncHttpx.post(url, headers=header, **kwargs)
        response.raise_for_status()
        raw_data = cls.__format_data(response)
        data = raw_data.data
        if not raw_data.success and (
            captcha_solver and isinstance(data, dict) and data.get("geeTest")
        ):
            seccode_data = await solve_captcha(url)
            if isinstance(seccode_data, CaptchaResult):
                seccode_data = model_dump(seccode_data)
            elif isinstance(seccode_data, CallResult):
                seccode_data = json.dumps(seccode_data)
            # 重试数据准备
            retry_data = data.copy() if data else {}
            retry_data["geeTestData"] = seccode_data
            return await cls.call_post(url, header=header, data=retry_data)

        return raw_data
