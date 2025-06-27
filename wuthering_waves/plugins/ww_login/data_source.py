import asyncio
import hashlib
from pathlib import Path
import uuid

import nonebot
from nonebot.adapters import Bot

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from ...config import GAME_NAME, LOG_COMMAND, WEB_PREFIX, config
from ...utils.pattern import CODE_PATTERN, MOBILE_PATTERN
from ...utils.utils import QrCodeUtils, TimedCache, get_public_ip
from ...utils.waves_api import WavesApi
from ...ww_handler import WavesHandler

driver = nonebot.get_driver()

cache = TimedCache(timeout=600, maxsize=10)

LOGIN_ERROR_MESSAGE = f"{GAME_NAME} 登录失败\n1.是否注册过库街区\n2.库街区能否查询当前{GAME_NAME}特征码数据\n"

QR_RESULT_FORMAT = """
{} 用户ID：【{}】
请扫描二维码获取登录链接
""".strip()

NORMAL_RESULT_FORMAT = """
{} 用户ID：【{}】
登录链接(10分钟内有效)：
{}
""".strip()


class LoginManager:
    @classmethod
    def __is_valid_chinese_phone_number(cls, phone_number: str) -> bool:
        """验证是否为有效的中国大陆手机号码

        参数:
            phone_number: 手机号码

        返回:
            bool: 是否为有效的中国大陆手机号码
        """
        if not phone_number:
            return False
        return MOBILE_PATTERN.match(phone_number) is not None

    @classmethod
    def __is_valid_code(cls, code: str) -> bool:
        """验证是否为有效的验证码

        参数:
            code: 验证码

        返回:
            bool: 是否为有效的验证码
        """
        return CODE_PATTERN.match(code) is not None if code else False

    @classmethod
    async def get_login_url(cls) -> str:
        """获取登录URL

        返回:
            str: 登录URL
        """
        host = (
            "127.0.0.1"
            if config.is_test
            else await get_public_ip() or driver.config.host
        )
        port = driver.config.port
        return f"http://{host}:{port}"

    @classmethod
    def get_token(cls, user_id: str) -> str:
        """获取token

        参数:
            user_id: 用户ID

        返回:
            str: token
        """
        return hashlib.sha256(user_id.encode()).hexdigest()[:8]

    @classmethod
    async def get_login(cls, user_id: str, user_token: str) -> list[str | Path]:
        """获取登录信息

        参数:
            user_id: 用户ID

        返回:
            list[str | Path]: 登录信息
        """
        url = f"{await cls.get_login_url()}{WEB_PREFIX}/login/{user_token}"
        if not config.login.qr_login:
            return [NORMAL_RESULT_FORMAT.format(GAME_NAME, user_id, url)]
        path = QrCodeUtils.generate_qr_code(url)
        return [QR_RESULT_FORMAT.format(GAME_NAME, user_id), path]

    @classmethod
    async def code_login(
        cls, bot: Bot, user_id: str, group_id: str | None, text: str
    ) -> str:
        """验证码登录

        参数:
            bot: Bot
            user_id: 用户ID
            group_id: 群ID
            text: 手机号 验证码

        返回:
            str: 登录结果
        """
        mobile, code = text.split()
        if not cls.__is_valid_chinese_phone_number(mobile) or not cls.__is_valid_code(
            code
        ):
            return "手机号+验证码登录失败\n\n请参照以下格式:\n WW登录 手机号 验证码"

        did = str(uuid.uuid4()).upper()
        result = await WavesApi.login(mobile, code, did)
        if not result.success:
            return (
                LOGIN_ERROR_MESSAGE
                if result.msg == "系统繁忙，请稍后再试"
                else result.msg
            )
        token = result.data.token
        await WavesHandler.add_cookie(user_id, token, did)
        return "登录成功"

    @classmethod
    async def page_login(cls, bot: Bot, user_id: str, group_id: str | None) -> str:
        """页面登录

        参数:
            bot: Bot
            user_id: 用户ID
            group_id: 群ID

        """

        token = cls.get_token(user_id)

        await PlatformUtils.send_message(
            bot,
            user_id,
            group_id,
            MessageUtils.build_message(*await cls.get_login(user_id, token)),
        )

        result = cache.get(token)
        if isinstance(result, dict):
            return ""

        future = asyncio.get_event_loop().create_future()
        data = {"mobile": -1, "code": -1, "user_id": user_id, "future": future}
        cache.set(token, data)
        text = ""
        try:
            # 等待结果或超时
            result = await asyncio.wait_for(future, timeout=600)
            text = f"{result['mobile']} {result['code']}"
        except asyncio.TimeoutError:
            cache.delete(token)
            await PlatformUtils.send_message(
                bot, user_id, group_id, "登录超时，请重新尝试"
            )
        except Exception as e:
            logger.error("登录过程中出现错误", LOG_COMMAND, session=user_id, e=e)
            cache.delete(token)
            await PlatformUtils.send_message(
                bot, user_id, group_id, "登录过程中出现错误，请稍后重试"
            )
        return await cls.code_login(bot, user_id, group_id, text)
