import inspect
import random
import string

from zhenxun.services.log import logger

from ...config import LOG_COMMAND
from ...models.waves_user import WavesUser
from ...utils.utils import get_public_ip

KURO_VERSION = "2.5.0"
KURO_VERSION_CODE = "2500"


def generate_random_string(length: int = 32) -> str:
    """生成随机字符串

    参数:
        length: 字符串长度

    return:
        str: 随机字符串
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def generate_random_ipv6_manual():
    """生成随机IPv6地址"""
    return ":".join([hex(random.randint(0, 0xFFFF))[2:].zfill(4) for _ in range(8)])


def generate_random_ipv4_manual():
    """生成随机IPv4地址"""
    return ".".join([str(random.randint(0, 255)) for _ in range(4)])


async def get_common_header(platform: str = "ios") -> dict:
    """获取通用头"""
    devCode = generate_random_string()
    return {
        "source": platform,
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "devCode": devCode,
        "X-Forwarded-For": generate_random_ipv6_manual(),
        "version": KURO_VERSION,
    }


async def get_headers_h5() -> dict:
    """获取H5头"""
    devCode = generate_random_string()
    return {
        "source": "h5",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        " Edg/136.0.0.0",
        "devCode": devCode,
        "X-Forwarded-For": generate_random_ipv6_manual(),
        "version": KURO_VERSION,
    }


async def get_headers_ios() -> dict:
    """获取iOS头"""
    ip = await get_public_ip()
    return {
        "source": "ios",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko)  KuroGameBox/2.5.0",
        "devCode": f"{ip}, Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X)"
        " AppleWebKit/605.1.15 (KHTML, like Gecko)  KuroGameBox/2.5.0",
        "X-Forwarded-For": generate_random_ipv6_manual(),
    }


async def get_headers(
    cookie: str | None = None,
    platform: str | None = None,
    role_id: str | None = None,
) -> dict:
    """获取请求头

    参数:
        cookie: 库洛cookie
        platform: 平台
        role_id: 鸣潮uid

    返回:
        dict: 请求头
    """
    if not cookie and not platform:
        return await get_headers_h5()

    bat = ""
    did = ""
    platform = "ios"
    user = None
    if cookie:
        if role_id:
            user = await WavesUser.get_or_none(role_id=role_id, cookie=cookie)
        if not user:
            user = await WavesUser.get_or_none(cookie=cookie)

        if user:
            platform = user.platform
            bat = user.access_token
            did = user.device_id
            role_id = user.role_id

            logger.debug(
                f"[get_headers.self.{inspect.stack()[1].function}]"
                f" [role_id:{role_id}] 获取成功: did: {did} bat: {bat}",
                LOG_COMMAND,
            )

    if platform == "ios":
        header = await get_headers_ios()
    else:
        header = await get_common_header(platform or "ios")
    if bat:
        header.update({"b-at": bat})
    if did:
        header.update({"did": did})
    if role_id:
        header.update({"roleId": role_id})
    return header
