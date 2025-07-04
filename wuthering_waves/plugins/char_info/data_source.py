from ...config import GAME_NAME
from ...exceptions import WavesException
from ...handles.char import CharHandler
from ...handles.cookie import CookieHandler
from ...models.waves_user import WavesUser
from ...utils.manager.entity_manager import EntityManager
from ...utils.utils import TimedCache
from ...waves_api import WavesApi
from ...waves_api.api.user.models import BaseUserData
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_100, WAVES_CODE_102

cache = TimedCache(timeout=60)


def get_default_base_user_data(role_id: str):
    return BaseUserData(
        name="库洛交个朋友",
        id=int(role_id),
        level=100,
        worldLevel=10,
        creatTime=1739375719,
        achievementCount=0,
        achievementStar=0,
        activeDays=1,
        bigCount=0,
        boxList=[],
        chapterId=1,
        energy=160,
        liveness=0,
        livenessMaxCount=100,
        livenessUnlock=True,
        maxEnergy=160,
        phantomBoxList=[],
        roleNum=0,
        rougeIconUrl=None,
        rougeScore=None,
        rougeScoreLimit=None,
        rougeTitle=None,
        showBirthIcon=False,
        showToGuest=True,
        smallCount=0,
        storeEnergy=0,
        storeEnergyIconUrl="",
        storeEnergyLimit=0,
        storeEnergyTitle="",
        treasureBoxList=[],
        weeklyInstCount=0,
        weeklyInstCountLimit=0,
        weeklyInstIconUrl="",
        weeklyInstTitle="",
    )


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
        refresh_chars_ids = "all"
        if isinstance(refresh_chars, list):
            refresh_chars_ids = [
                char_id
                for r in refresh_chars
                if (char_id := EntityManager.name_to_id(r))
            ]
        char_list, changed_roles, unchanged_roles = await CharHandler.refresh_char(
            user_id, role_id, cookie, is_self, refresh_chars_ids
        )
        cls.__add_cache(role_id)

    @classmethod
    async def get_char_detail(
        cls, user_id: str, role_id: str | None, char_name: str, is_limit_query: bool
    ):
        if not role_id:
            role_ids = await WavesUser.get_role_ids(user_id)
            if not role_ids:
                raise WavesException(ERROR_CODE[WAVES_CODE_100])
            role_id = role_ids[0]
        alias_name = EntityManager.get_char_alias(char_name)
        char_id = EntityManager.name_to_id(char_name)
        if not char_id or not alias_name:
            raise WavesException(
                f"{GAME_NAME} 角色名【{char_name}】无法找到, "
                "可能暂未适配, 请先检查输入是否正确！\n"
            )
        is_online_char = False
        if not is_limit_query:
            is_online_char = await CharHandler.is_online_char(user_id, role_id, char_id)
            cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
            if not cookie:
                raise WavesException(ERROR_CODE[WAVES_CODE_102])
            account_info = (await WavesApi.get_base_info(role_id, cookie)).data
            force_resource_id = None
        else:
            account_info = get_default_base_user_data(role_id)
            force_resource_id = char_id
