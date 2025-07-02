from ....base_models import WwBaseResponse
from ...const import (
    GAME_ID,
    ONLINE_LIST_ROLE,
    ROLE_DATA_URL,
    ROLE_DETAIL_URL,
    ROLE_LIST_URL,
)
from ...headers import get_common_header, get_headers
from ..call import CallApi, get_access_token, get_server_id, login_platform
from ..login import login_status_check
from .models import CharDetailData, RoleDataContent, RoleInfo, RoleItem


class RoleApi:
    @classmethod
    @login_status_check()
    async def role_list(
        cls, cookie: str, device_id: str
    ) -> tuple[WwBaseResponse[list[RoleInfo]], str]:
        """获取角色（用户列表）列表

        参数:
            cookie: 登录token
            device_id: 设备id

        返回:
            tuple[WwBaseResponse[list[RoleInfo]], str]: 角色列表, 平台
        """
        platform = login_platform()
        header = await get_common_header(platform=platform)
        header.update(
            {
                "token": cookie,
                "devCode": device_id,
            }
        )
        response = await CallApi.call_post(
            ROLE_LIST_URL, header=header, data={"gameId": GAME_ID}
        )
        # 兼容pydantic 1.x
        response.data = [RoleInfo(**v) for v in response.data]
        return response, platform

    @classmethod
    @login_status_check()
    async def char_list(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[RoleDataContent]:
        """获取角色（游戏内角色列表）数据

        参数:
            role_id: 角色（用户）ID
            cookie: 登录token
            server_id: 服务器ID

        返回:
            WwBaseResponse[RoleDataContent]: 角色数据
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
        response.data = RoleDataContent(**response.data)
        return response

    @classmethod
    @login_status_check()
    async def get_char_detail_info(
        cls, char_id: str, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[CharDetailData]:
        """获取角色（游戏内角色）详情信息

        参数:
            char_id: 角色ID
            role_id: 角色（用户）ID
            cookie: 登录token
            server_id: 服务器ID

        返回:
            WwBaseResponse[CharDetailData]: 角色详情信息
        """
        header = await get_headers(cookie, role_id=role_id)
        hd_role_id = header.get("role_id")
        if hd_role_id != role_id:
            access_token = await get_access_token(
                role_id, cookie, header.get("did", ""), server_id
            )
            header.update({"b-at": access_token})
        response = await CallApi.call_post(
            ROLE_DETAIL_URL,
            header=header,
            data={
                "gameId": GAME_ID,
                "serverId": server_id or get_server_id(role_id),
                "roleId": role_id,
                "channelId": "19",
                "countryCode": "1",
                "id": char_id,
            },
        )
        response.data = CharDetailData(**response.data)
        return response

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
