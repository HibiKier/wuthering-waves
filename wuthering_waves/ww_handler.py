from zhenxun.services.log import logger

from .config import LOG_COMMAND
from .models.waves_user import WavesUser
from .utils.cache import token_cache
from .utils.exceptions import APICallException, WavesException
from .utils.waves_api import WavesApi
from .utils.waves_api.api import GAME_ID
from .utils.waves_api.error_code import get_error_message


class WavesHandler:
    @classmethod
    async def add_cookie(cls, user_id: str, cookie: str, device_id: str):
        """添加或更新用户cookie

        参数:
            user_id: 用户id
            cookie: cookie
            device_id: 设备id

        异常:
            APICallException: 请求调用错误
            WavesException: 未获取到用户角色
            APICallException: 请求调用错误
        """
        response, platform = await WavesApi.role_list(cookie, device_id)
        if not response.success:
            raise APICallException(
                response.url,
                response.code,
                response.msg or get_error_message(response.code),
            )
        role_list = [r for r in response.data if r.game_id == GAME_ID]
        if not role_list:
            logger.warning("未获取到任何登录用户，登录失败", LOG_COMMAND)
            raise WavesException("未获取到任何登录用户，登录失败")
        for role in role_list:
            user, _ = await WavesUser.get_or_create(
                user_id=user_id, role_id=role.role_id
            )
            if token_cache.get(role.role_id):
                access_token = token_cache.get(role.role_id)
            else:
                token_response = await WavesApi.request_token(
                    role.role_id, cookie, device_id, role.server_id
                )
                if not token_response.success:
                    raise APICallException(
                        token_response.url,
                        token_response.code,
                        token_response.msg or get_error_message(token_response.code),
                    )
                access_token = token_response.data.access_token
                token_cache.set(role.role_id, access_token)
            user.access_token = access_token
            user.platform = platform
            user.role_id = role.role_id
            user.device_id = device_id
            user.access_token = access_token
            await user.save(
                update_fields=["access_token", "platform", "role_id", "access_token"]
            )
