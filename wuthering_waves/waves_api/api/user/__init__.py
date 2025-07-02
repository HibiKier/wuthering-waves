from ....base_models import WwBaseResponse
from ...api.login import login_status_check
from ...const import BASE_DATA_URL, ROLE_DATA_URL, TOWER_DETAIL_URL
from ...headers import get_headers
from ..call import CallApi, get_access_token
from .models import BaseUserData, RoleListData, TowerData


class UserApi:
    @classmethod
    @login_status_check()
    async def get_base_info(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[BaseUserData]:
        """获取用户基础信息

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            server_id: 服务器ID

        返回:
            WwBaseResponse[BaseUserData]: 用户基础信息
        """
        header = await get_headers(cookie, role_id=role_id)
        hd_role_id = header.get("role_id")
        if hd_role_id != role_id:
            access_token = await get_access_token(
                role_id, cookie, header.get("did", ""), server_id
            )
            header.update({"b-at": access_token})
        response = await CallApi.call_post(
            BASE_DATA_URL,
            header=header,
            data=CallApi.default_params(role_id, server_id),
        )
        response.data = BaseUserData(**response.data)
        return response

    @classmethod
    @login_status_check()
    async def get_role_info(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[RoleListData]:
        """获取鸣潮角色信息

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            server_id: 服务器ID

        返回:
            WwBaseResponse[RoleListData]: 角色信息
        """
        header = await get_headers(cookie, role_id=role_id)
        hd_role_id = header.get("role_id")
        if hd_role_id != role_id:
            access_token = await get_access_token(
                role_id, cookie, header.get("did", ""), server_id
            )
            header.update({"b-at": access_token})
        response = await CallApi.call_post(
            ROLE_DATA_URL,
            header=header,
            data=CallApi.default_params(role_id, server_id),
        )
        response.data = RoleListData(**response.data)
        return response

    @classmethod
    @login_status_check()
    async def get_abyss_data(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[TowerData]:
        """获取深境数据

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            server_id: 服务器ID

        返回:
            WwBaseResponse[TowerData]: 深境数据
        """
        header = await get_headers(cookie, role_id=role_id)
        response = await CallApi.call_post(
            TOWER_DETAIL_URL,
            header=header,
            data=CallApi.default_params(role_id, server_id),
        )
        response.data = TowerData(**response.data)
        return response

    @classmethod
    @login_status_check()
    async def get_abyss_index(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[TowerData]:
        """获取深境索引数据

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            server_id: 服务器ID

        返回:
            WwBaseResponse[TowerData]: 深境索引数据
        """
        header = await get_headers(cookie, role_id=role_id)
        hd_role_id = header.get("role_id")
        if hd_role_id != role_id:
            access_token = await get_access_token(
                role_id, cookie, header.get("did", ""), server_id
            )
            header.update({"b-at": access_token})
        response = await CallApi.call_post(
            TOWER_DETAIL_URL,
            header=header,
            data=CallApi.default_params(role_id, server_id),
        )
        response.data = TowerData(**response.data)
        return response
