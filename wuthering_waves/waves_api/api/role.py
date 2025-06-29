from ...base_models import WwBaseResponse
from ..api.call import CallApi, login_platform
from ..const import GAME_ID, ROLE_LIST_URL
from ..headers import get_common_header
from ..models import RoleInfo


class RoleApi:
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
        platform = login_platform()
        header = await get_common_header(platform=platform)
        header.update(
            {
                "token": token,
                "devCode": did,
            }
        )
        response = await CallApi.call_post(
            ROLE_LIST_URL, header=header, data={"gameId": GAME_ID}
        )
        # 兼容pydantic 1.x
        response.data = [RoleInfo(**v) for v in response.data]
        return response, platform
