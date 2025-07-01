from ..base_models import WwBaseResponse
from .api.login import LoginApi
from .api.login.models import LoginResult, RequestToken
from .api.role import RoleApi
from .api.role.models import RoleInfo
from .api.user import UserApi
from .api.user.models import BaseUserData, RoleListData, TowerData


class WavesApi:
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
        return await LoginApi.login(mobile, code, did)

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
        return await RoleApi.role_list(token, did)

    @classmethod
    async def request_token(
        cls, role_id: str, cookie: str, device_id: str, server_id: str | None = None
    ) -> WwBaseResponse[RequestToken]:
        """获取access_token

        参数:
            role_id: 角色id
            token: 登录token
            did: 设备id
            server_id: 服务器id

        返回:
            WwBaseResponse[RequestToken]: 获取access_token
        """
        return await LoginApi.request_token(role_id, cookie, device_id, server_id)

    @classmethod
    async def login_log(cls, role_id: str, token: str) -> WwBaseResponse[bool]:
        """登录状态检查

        参数:
            role_id: 角色id
            token: 登录token

        返回:
            WwBaseResponse[bool]: 登录日志查询结果
        """
        return await LoginApi.login_log(role_id, token)

    @classmethod
    async def get_base_info(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[BaseUserData]:
        """获取用户基础信息

        参数:
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[BaseUserData]: 用户基础信息
        """
        return await UserApi.get_base_info(role_id, cookie, server_id)

    @classmethod
    async def get_role_info(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[RoleListData]:
        """获取角色信息

        参数:
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[RoleListData]: 角色信息
        """
        return await UserApi.get_role_info(role_id, cookie, server_id)

    @classmethod
    async def get_abyss_data(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[TowerData]:
        """获取深境数据

        参数:
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[TowerData]: 深境数据
        """
        return await UserApi.get_abyss_data(role_id, cookie, server_id)

    @classmethod
    async def get_abyss_index(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[TowerData]:
        """获取深境数据

        参数:
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[TowerData]: 深境数据
        """
        return await UserApi.get_abyss_index(role_id, cookie, server_id)
