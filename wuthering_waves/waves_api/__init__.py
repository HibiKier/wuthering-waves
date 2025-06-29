from ..base_models import WwBaseResponse
from .api.login import LoginApi
from .api.role import RoleApi
from .models import LoginResult, RequestToken, RoleInfo


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
        cls, role_id: str, token: str, did: str, server_id: str | None = None
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
        return await LoginApi.request_token(role_id, token, did, server_id)

    @classmethod
    async def login_log(cls, rold_id: str, token: str) -> WwBaseResponse[bool]:
        """登录状态检查

        参数:
            rold_id: 角色id
            token: 登录token

        返回:
            WwBaseResponse[bool]: 登录日志查询结果
        """
        return await LoginApi.login_log(rold_id, token)
