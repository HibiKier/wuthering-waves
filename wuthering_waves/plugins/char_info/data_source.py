from zhenxun.builtin_plugins.wuthering_waves.waves_api import WavesApi

from ...exceptions import WavesException
from ...handles.cookie import CookieHandler
from ...utils.utils import TimedCache
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_102

cache = TimedCache(timeout=60)


class CharInfoDataSource:
    @classmethod
    def __is_allow_refresh(cls, rold_id: str) -> bool:
        """
        检查是否允许刷新角色信息

        参数:
            rold_id: 角色ID

        返回:
            bool: 是否允许刷新角色信息
        """
        return bool(cache.get(rold_id))

    @classmethod
    def __add_cache(cls, user_id: str, rold_id: str):
        """
        添加角色信息缓存

        参数:
            rold_id: 角色ID
        """
        if not cache.get(rold_id):
            cache.set(rold_id, 1)

    @classmethod
    async def get_char_info(cls, user_id: str, rold_id: str):
        if not cls.__is_allow_refresh(rold_id):
            raise WavesException("角色信息刷新过于频繁，请稍后再试")
        cookie, is_selfw = await CookieHandler.get_cookie(user_id, rold_id)
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        char_info = await WavesApi.get_base_info(rold_id, cookie)
        return char_info
