from ...exceptions import WavesException
from ...handles.cookie import CookieHandler
from ...handles.role import RoleHandler
from ...models.waves_user import WavesUser
from ...utils.manager.entity_manager import (
    EntityManager,
)
from ...utils.utils import TimedCache
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_100, WAVES_CODE_102

cache = TimedCache(timeout=60)


class CharInfoDataSource:
    @classmethod
    def __is_allow_refresh(cls, role_id: str) -> bool:
        """
        检查是否允许刷新角色信息

        参数:
            role_id: 角色ID

        返回:
            bool: 是否允许刷新角色信息
        """
        return not bool(cache.get(role_id))

    @classmethod
    def __add_cache(cls, role_id: str):
        """
        添加角色信息缓存

        参数:
            role_id: 角色ID
        """
        if not cache.get(role_id):
            cache.set(role_id, 1)

    @classmethod
    async def get_char_info(
        cls,
        user_id: str,
        role_id: str | None = None,
        refresh_chars: list[str] | str = "all",
    ):
        if not role_id:
            role_ids = await WavesUser.get_role_ids(user_id)
            if not role_ids:
                raise WavesException(ERROR_CODE[WAVES_CODE_100])
            role_id = role_ids[0]
        if not cls.__is_allow_refresh(role_id):
            raise WavesException("角色信息刷新过于频繁，请稍后再试")
        cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        if isinstance(refresh_chars, list):
            refresh_chars = [
                char_id
                for r in refresh_chars
                if (char_id := EntityManager.name_to_id(r))
            ]
        char_list, changed_roles, unchanged_roles = await RoleHandler.refresh_char(
            user_id, role_id, cookie, is_self, refresh_chars
        )
        cls.__add_cache(role_id)
