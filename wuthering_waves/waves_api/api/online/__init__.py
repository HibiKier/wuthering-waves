from ....base_models import WwBaseResponse
from ...const import ONLINE_LIST_ROLE, ONLINE_LIST_WEAPON
from ...headers import get_headers
from ..call import CallApi
from ..login import login_status_check
from .models import RoleItem, WeaponItem


class OnlineApi:
    @classmethod
    @login_status_check()
    async def get_online_list_role(cls, cookie: str) -> WwBaseResponse[list[RoleItem]]:
        """所有的角色列表

        参数:
            cookie: 登录token

        返回:
            WwBaseResponse[list[RoleItem]]: 角色列表
        """
        header = await get_headers(cookie)
        response = await CallApi.call_post(ONLINE_LIST_ROLE, header=header)
        response.data = [RoleItem(**v) for v in response.data]
        return response

    @classmethod
    @login_status_check()
    async def get_online_list_weapon(
        cls, cookie: str
    ) -> WwBaseResponse[list[WeaponItem]]:
        """所有的武器列表

        参数:
            cookie: 登录token

        返回:
            WwBaseResponse[list[WeaponItem]]: 武器列表
        """
        header = await get_headers(cookie)
        response = await CallApi.call_post(ONLINE_LIST_WEAPON, header=header)
        response.data = [WeaponItem(**v) for v in response.data]
        return response
