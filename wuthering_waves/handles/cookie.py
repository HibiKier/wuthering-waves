from typing import ClassVar

from zhenxun.services.log import logger

from ..config import LOG_COMMAND
from ..exceptions import APICallException, LoginStatusCheckException, WavesException
from ..models.waves_user import WavesUser
from ..utils.emuns import CookieStatus
from ..waves_api import WavesApi
from ..waves_api.api.login import LoginApi
from ..waves_api.const import GAME_ID, SUCCESS_CODE
from ..waves_api.error_code import get_error_message


class CookieHandler:
    _bat_cache: ClassVar[dict[str, str]] = {}

    @classmethod
    async def get_access_token(
        cls, role_id: str, cookie: str, device_id: str, server_id: str | None = None
    ) -> str:
        """获取access_token

        参数:
            role_id: 角色id
            cookie: 登录token
            device_id: 设备id
            server_id: 服务器id

        异常:
            APICallException: 请求调用错误

        返回:
            str: access_token
        """
        if role_id in cls._bat_cache:
            return cls._bat_cache[role_id]
        response = await WavesApi.request_token(role_id, cookie, device_id, server_id)
        if not response.success and response.code not in SUCCESS_CODE:
            raise APICallException(
                response.url,
                response.code,
                response.msg or get_error_message(response.code),
            )
        cls._bat_cache[role_id] = response.data.access_token
        return response.data.access_token

    @classmethod
    async def get_cookie(
        cls, user_id: str, role_id: str | None = None
    ) -> tuple[str | None, bool]:
        """获取cookie

        参数:
            user_id: 用户id
            role_id: 角色id

        返回:
            tuple[str | None, bool]: cookie, 是否为自身的cookie
        """
        # 先获取用户自身的所有cookie
        if role_id:
            result = await WavesUser.get_user_cookie(role_id)
            if result:
                return result.cookie, True
        results = await WavesUser.get_user_cookies(user_id)
        for result in results:
            try:
                if await LoginApi.login_log(
                    role_id=result["role_id"], cookie=result["cookie"]
                ):
                    return result["cookie"], True
            except LoginStatusCheckException as e:
                logger.warning(
                    f"role_id: 【{result['role_id']}】登录已失效...", LOG_COMMAND, e=e
                )
        # 如果自身所有cookie都失效，则随机获取有效cookie
        results = await WavesUser.random_cookie(100)
        for result in results:
            try:
                if await LoginApi.login_log(
                    role_id=result.role_id, cookie=result.cookie
                ):
                    return result.cookie, False
            except LoginStatusCheckException as e:
                logger.warning(
                    f"role_id: 【{result.role_id}】登录已失效...", LOG_COMMAND, e=e
                )
        return None, False

    @classmethod
    async def add_user_cookie(cls, user_id: str, cookie: str, device_id: str):
        """添加或更新用户cookie

        参数:
            user_id: 用户id
            cookie: cookie
            device_id: 设备id

        异常:
            APICallException: 请求调用错误
            WavesException: 未获取到用户角色
        """
        response, platform = await WavesApi.role_list(cookie, device_id)
        if not response.success:
            raise APICallException(
                response.url,
                response.code,
                response.msg or get_error_message(response.code),
            )

        # 过滤出匹配游戏ID的角色列表
        role_list = [r for r in response.data if r.game_id == GAME_ID]

        if not role_list:
            logger.warning(
                "未获取到任何登录用户，登录失败", LOG_COMMAND, session=user_id
            )
            raise WavesException("未获取到任何登录用户，登录失败")

        role = role_list[0]

        user, _ = await WavesUser.get_or_create(user_id=user_id, role_id=role.role_id)
        user.access_token = await cls.get_access_token(
            role.role_id, cookie, device_id, role.server_id
        )
        user.platform = platform
        user.role_id = role.role_id
        user.device_id = device_id
        user.cookie = cookie
        user.cookie_status = CookieStatus.LOGIN_SUCCESS
        await user.save(
            update_fields=[
                "access_token",
                "platform",
                "role_id",
                "access_token",
                "cookie",
                "cookie_status",
            ]
        )
