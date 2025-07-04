from ....base_models import WwBaseResponse
from ....waves_api.api.call import CallApi
from ....waves_api.const import CALCULATOR_REFRESH_DATA_URL
from ....waves_api.headers import get_headers


class OtherApi:
    @classmethod
    async def calculator_refresh_data(
        cls, role_id: str, cookie: str, service_id: str | None = None
    ) -> WwBaseResponse[bool]:
        """刷新养成数据

        参数:
            role_id: 角色ID
            cookie: 用户cookie
            service_id: 服务器ID

        返回:
            WwBaseResponse[bool]: 是否刷新成功
        """
        headers = await get_headers(cookie, role_id=role_id)
        return await CallApi.call_post(
            CALCULATOR_REFRESH_DATA_URL,
            header=headers,
            data=CallApi.default_params(role_id=role_id, server_id=service_id),
        )
