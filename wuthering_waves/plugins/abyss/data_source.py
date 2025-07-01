from ...exceptions import WavesException
from ...handles.cookie import CookieHandler
from ...models.waves_user import WavesUser
from ...waves_api import WavesApi
from ...waves_api.api.user.models import TowerData
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_102


class AbyssDataSource:
    @classmethod
    def __get_difficulty(cls, area: str) -> str:
        """获取深境区难度"""
        difficulty_name = "深境区"
        if "超载" in area:
            difficulty_name = "超载区"
        elif "稳定" in area:
            difficulty_name = "稳定区"
        elif "实验" in area:
            difficulty_name = "实验区"
        return difficulty_name

    @classmethod
    async def __get_abyss_data(
        cls, role_id: str, cookie: str, is_self: bool
    ) -> TowerData:
        """获取深境数据

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            is_self: 是否为当前角色

        返回:
            TowerData: 深境数据
        """
        if is_self:
            response = await WavesApi.get_abyss_data(role_id, cookie)
        else:
            response = await WavesApi.get_abyss_index(role_id, cookie)
        if not response.data.difficulty_list:
            raise WavesException("当前暂无深渊数据")
        if not response.data.is_unlock:
            if is_self:
                raise WavesException("当前深渊未解锁或未进行登录")
            else:
                raise WavesException("当前深渊未解锁")

        return response.data

    @classmethod
    async def get_abyss(cls, area: str, user_id: str, role_id: str | None):
        if not role_id:
            role_ids = await WavesUser.get_role_ids(user_id)
            if not role_ids:
                raise WavesException("还未绑定任何鸣潮特征码")
            role_id = role_ids[0]
        cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(f"{ERROR_CODE[WAVES_CODE_102]}")
        difficulty_name = cls.__get_difficulty(area)
        account_info = await WavesApi.get_base_info(role_id, cookie)
        role_info = await WavesApi.get_role_info(role_id, cookie)
        abyss_data = await cls.__get_abyss_data(role_id, cookie, is_self)
