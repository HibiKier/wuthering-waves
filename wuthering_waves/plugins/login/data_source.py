import asyncio
import hashlib
from pathlib import Path
import uuid

import async_timeout
import nonebot
from nonebot.adapters import Bot

from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from ...config import GAME_NAME, LOG_COMMAND, WEB_PREFIX, config
from ...handles.cookie import CookieHandler
from ...utils.pattern import CODE_PATTERN, MOBILE_PATTERN
from ...utils.utils import QrCodeUtils, TimedCache, get_public_ip
from ...waves_api import WavesApi

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

# 添加常量定义
LOGIN_TIMEOUT = 600  # 登录超时时间（秒）
POLL_INTERVAL = 0.1  # 轮询间隔（秒）
LOGIN_DATA_INIT = {"mobile": -1, "code": -1}


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
    async def code_login(cls, user_id: str, text: str) -> str:
        """验证码登录

        参数:
            user_id: 用户ID
            text: 手机号 验证码

        返回:
            str: 登录结果
        """
        mobile, code = text.split()
        if not cls.__is_valid_chinese_phone_number(mobile) or not cls.__is_valid_code(
            code
        ):
            return "手机号+验证码登录失败\n\n请参照以下格式:\n ww登录 手机号 验证码"

        device_id = str(uuid.uuid4()).upper()
        result = await WavesApi.login(mobile, code, device_id)
        if not result.success:
            return (
                LOGIN_ERROR_MESSAGE
                if result.msg == "系统繁忙，请稍后再试"
                else result.msg
            )
        token = result.data.token
        await CookieHandler.add_user_cookie(user_id, token, device_id)
        return "登录成功"

    @classmethod
    async def page_login(cls, bot: Bot, user_id: str, group_id: str | None) -> str:
        """页面登录

        参数:
            bot: Bot
            user_id: 用户ID
            group_id: 群ID

        返回:
            str: 登录结果
        """
        token = cls.get_token(user_id)

        try:
            # 发送登录信息
            await PlatformUtils.send_message(
                bot,
                user_id,
                group_id,
                MessageUtils.build_message(*await cls.get_login(user_id, token)),
            )

            # 检查是否已有完整的登录数据
            result = cache.get(token)
            if (
                result
                and cls._is_complete_login_data(result)
                and isinstance(result, dict)
            ):
                text = f"{result['mobile']} {result['code']}"
                cache.delete(token)
                return await cls.code_login(user_id, text)

            # 创建新的登录会话
            data = {**LOGIN_DATA_INIT, "user_id": user_id}
            cache.set(token, data)

            # 等待登录结果
            text = await cls._wait_for_login_completion(bot, user_id, group_id, token)

            # 执行登录
            return await cls.code_login(user_id, text)

        except Exception as e:
            # 确保清理缓存
            cache.delete(token)
            logger.error("页面登录过程中出现错误", LOG_COMMAND, session=user_id, e=e)
            await PlatformUtils.send_message(
                bot, user_id, group_id, "用户登录过程中出现错误..."
            )
            return "登录过程中出现错误，请稍后重试"

    @classmethod
    def _is_complete_login_data(cls, result) -> bool:
        """检查是否为完整的登录数据"""
        if not isinstance(result, dict) or result is None:
            return False
        return result.get("mobile") != -1 and result.get("code") != -1

    @classmethod
    async def _wait_for_login_completion(
        cls, bot: Bot, user_id: str, group_id: str | None, token: str
    ) -> str:
        """等待登录完成

        参数:
            bot: Bot
            user_id: 用户ID
            group_id: 群ID
            token: 登录token

        返回:
            str: 登录信息文本

        异常:
            asyncio.TimeoutError: 登录超时
        """
        try:
            async with async_timeout.timeout(LOGIN_TIMEOUT):
                while True:
                    result = cache.get(token)

                    if result is None:
                        # 缓存被清理，说明超时
                        await cls._send_timeout_message(bot, user_id, group_id)
                        raise asyncio.TimeoutError("登录超时")

                    if cls._is_complete_login_data(result):
                        # 获取到完整的登录信息
                        if result and isinstance(result, dict):
                            text = f"{result['mobile']} {result['code']}"
                            cache.delete(token)
                            return text

                    # 等待后再次检查
                    await asyncio.sleep(POLL_INTERVAL)

        except asyncio.TimeoutError:
            # 超时处理
            cache.delete(token)
            await cls._send_timeout_message(bot, user_id, group_id)
            raise

    @classmethod
    async def _send_timeout_message(cls, bot: Bot, user_id: str, group_id: str | None):
        """发送超时消息"""
        await PlatformUtils.send_message(bot, user_id, group_id, "登录超时，请重新尝试")
