from zhenxun.builtin_plugins.wuthering_waves.config import LOG_COMMAND
from zhenxun.services.log import logger

from ..exceptions import LoginStatusCheckException
from ..models.waves_user import WavesUser
from ..waves_api.api.login import LoginApi


class CookieHandler:
    @classmethod
    async def get_cookie(cls, user_id: str) -> str | None:
        # 先获取用户自身的所有cookie
        results = await WavesUser.get_user_cookie(user_id=user_id)
        for result in results:
            try:
                await LoginApi.login_log(
                    rold_id=result["role_id"], cookie=result["cookie"]
                )
                return result["cookie"]
            except LoginStatusCheckException as e:
                logger.warning(
                    f"role_id: 【{result['role_id']}】登录已失效...", LOG_COMMAND, e=e
                )
        # 如果自身所有cookie都失效，则随机获取有效cookie
        return await WavesUser.random_cookie()
