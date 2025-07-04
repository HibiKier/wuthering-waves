from aiocache import cached

from ..base_models import WwBaseResponse
from .api.login import LoginApi
from .api.login.models import LoginResult, RequestToken
from .api.online import OnlineApi
from .api.online.models import RoleItem, WeaponItem
from .api.other import OtherApi
from .api.role import RoleApi
from .api.role.models import CharDetailData, RoleDataContent, RoleInfo, RoleProgress
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

    @classmethod
    async def get_char_detail_info(
        cls, char_id: str, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[CharDetailData]:
        """获取角色详情信息

        参数:
            char_id: 角色id
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[CharDetailData]: 角色详情信息
        """
        return await RoleApi.get_char_detail_info(char_id, role_id, cookie, server_id)

    @classmethod
    async def get_char_list(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[RoleDataContent]:
        """获取角色列表

        参数:
            role_id: 角色id
            cookie: 登录cookie
            server_id: 服务器id

        返回:
            WwBaseResponse[RoleDataContent]: 角色列表
        """
        return await RoleApi.char_list(role_id, cookie, server_id)

    @classmethod
    @cached(ttl=60 * 60 * 6)
    async def get_online_list_role(cls, cookie: str) -> WwBaseResponse[list[RoleItem]]:
        """获取已上线的角色

        参数:
            cookie: 登录cookie

        返回:
            WwBaseResponse[bool]: 已上线的角色
        """
        return await OnlineApi.get_online_list_role(cookie)

    @classmethod
    @cached(ttl=60 * 60 * 6)
    async def get_online_list_weapon(
        cls, cookie: str
    ) -> WwBaseResponse[list[WeaponItem]]:
        """获取已上线的武器

        参数:
            cookie: 登录cookie

        返回:
            WwBaseResponse[list[WeaponItem]]: 已上线的武器
        """
        return await OnlineApi.get_online_list_weapon(cookie)

    @classmethod
    async def calculator_refresh_data(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[bool]:
        """刷新养成数据"""
        return await OtherApi.calculator_refresh_data(role_id, cookie, server_id)

    @classmethod
    async def get_owned_role(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[list[int]]:
        """获取已拥有的角色

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            server_id: 服务器ID

        返回:
            WwBaseResponse[list[int]]: 已拥有的角色
        """
        return await RoleApi.get_owned_role(role_id, cookie, server_id)

    @classmethod
    async def get_develop_role_cultivate_status(
        cls, role_id: str, cookie: str, char_ids: list[int]
    ) -> WwBaseResponse[list[RoleProgress]]:
        """获取角色养成状态

        参数:
            role_id: 角色ID
            cookie: 登录cookie
            char_ids: 角色ID列表

        返回:
            WwBaseResponse[list[RoleProgress]]: 角色养成状态
        """
        return await RoleApi.get_develop_role_cultivate_status(
            role_id, cookie, char_ids
        )
