from typing import Any

from httpx import Response
from nonebot.compat import model_dump
import ujson as json

from zhenxun.services.log import logger
from zhenxun.utils.decorator.retry import Retry
from zhenxun.utils.http_utils import AsyncHttpx

from ...config import LOG_COMMAND
from ...utils.cache import cache_root
from ...utils.exceptions import APICallException
from .api import (
    GAME_ID,
    LOGIN_H5_URL,
    LOGIN_URL,
    NET_SERVER_ID_MAP,
    REQUEST_TOKEN,
    ROLE_LIST_URL,
    SERVER_ID,
    SERVER_ID_NET,
)
from .captcha import get_solver
from .captcha.base import CaptchaResult
from .captcha.errors import CaptchaError
from .error_code import (
    WAVES_CODE_999,
)
from .headers import get_common_header, get_headers
from .models import CallResult, LoginResult, RequestToken, RoleInfo, WwBaseResponse


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


class WavesApi:
    @classmethod
    def __format_data(cls, response: Response) -> WwBaseResponse:
        """格式化响应数据"""
        try:
            raw_data = WwBaseResponse(url=str(response.url), **response.json())
        except Exception as e:
            logger.warning(f"解析响应数据失败: {response.text}", LOG_COMMAND, e=e)
            try:
                raw_data = WwBaseResponse(
                    url=str(response.url),
                    code=WAVES_CODE_999,
                    data=json.loads(response.text),
                    msg=response.text,
                    success=False,
                )
            except Exception as e:
                logger.warning(f"解析响应数据失败: {response.text}", LOG_COMMAND, e=e)
                raw_data = WwBaseResponse(
                    url=str(response.url),
                    code=WAVES_CODE_999,
                    data=response.text,
                    msg=response.text,
                    success=False,
                )
        return raw_data

    @Retry.api()
    @classmethod
    async def call_post(
        cls, url: str, header: dict | None = None, **kwargs
    ) -> WwBaseResponse:
        """调用POST请求"""
        if not header:
            header = await get_headers()
        if header:
            header.pop("roleId")
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

    @classmethod
    async def login(
        cls, mobile: str, code: str, did: str
    ) -> WwBaseResponse[LoginResult]:
        """登录

        参数:
            mobile: 手机号
            code: 验证码
            did: 设备id

        返回:
            CallResult: 登录结果
        """
        platform = login_platform()
        header = await get_headers(platform=platform)
        data = {
            "mobile": mobile,
            "code": code,
            "devCode": did,
        }
        url = LOGIN_H5_URL if platform == "h5" else LOGIN_URL
        response = await cls.call_post(url, header=header, data=data)
        # 兼容pydantic 1.x
        response.data = LoginResult(**response.data)
        return response

    @classmethod
    async def role_list(
        cls, token: str, did: str
    ) -> tuple[WwBaseResponse[list[RoleInfo]], str]:
        """获取角色列表

        参数:
            token: 登录token
            did: 设备id

        返回:
            tuple[WwBaseResponse[list[RoleInfo]], str]: 角色列表, 平台
        """
        platform = login_platform()
        header = await get_common_header(platform=platform)
        header.update(
            {
                "token": token,
                "devCode": did,
            }
        )
        response = await cls.call_post(
            ROLE_LIST_URL, header=header, data={"gameId": GAME_ID}
        )
        # 兼容pydantic 1.x
        response.data = [RoleInfo(**v) for v in response.data]
        return response, platform

    @classmethod
    async def request_token(
        cls, role_id: str, token: str, did: str, server_id: str | None = None
    ) -> WwBaseResponse[RequestToken]:
        header = await get_headers(token, role_id=role_id)
        header.update({"token": token, "did": did, "b-at": ""})
        response = await cls.call_post(
            REQUEST_TOKEN,
            header=header,
            data={
                "serverId": server_id or get_server_id(role_id),
                "roleId": role_id,
            },
        )
        # 兼容pydantic 1.x
        response.data = RequestToken(**response.data)
        return response
