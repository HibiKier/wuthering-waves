from collections import OrderedDict
import contextlib
from pathlib import Path
import time
import uuid

from aiocache import cached
from qrcode.constants import ERROR_CORRECT_L
from qrcode.main import QRCode

from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx

from ..paths import QR_TEMP_PATH


@cached(ttl=86400)
async def get_public_ip() -> str | None:
    """获取公网IP"""
    with contextlib.suppress(Exception):
        response = await AsyncHttpx.get("https://event.kurobbs.com/event/ip", timeout=5)
        response.raise_for_status()
        return response.text

    with contextlib.suppress(Exception):
        response = await AsyncHttpx.get("https://api.ipify.org/?format=json", timeout=5)
        response.raise_for_status()
        return response.json()["ip"]

    with contextlib.suppress(Exception):
        response = await AsyncHttpx.get("https://httpbin.org/ip", timeout=5)
        response.raise_for_status()
        return response.json()["origin"]

    return None


class QrCodeUtils:
    @classmethod
    def generate_qr_code(cls, data: str, path: Path | None = None) -> Path:
        """生成二维码

        参数:
            data: 二维码数据
            path: 二维码保存路径
        """
        if path is None:
            path = QR_TEMP_PATH / f"{uuid.uuid4()}.png"
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=(255, 134, 36), back_color="white")
        img.save(path)
        return path


class TimedCache:
    """基于时间的缓存实现

    一个简单的基于时间的缓存实现，支持自动过期和容量限制。
    使用OrderedDict保持访问顺序，实现LRU（最近最少使用）淘汰策略。

    属性:
        timeout: 缓存项的过期时间（秒）
        maxsize: 缓存的最大容量
    """

    def __init__(self, timeout=60, maxsize=100):
        """初始化缓存

        参数:
            timeout: 缓存过期时间（秒），默认60秒
            maxsize: 缓存最大容量，默认100项
        """
        self.cache = OrderedDict()  # 使用OrderedDict保持访问顺序
        self.timeout = timeout
        self.maxsize = maxsize

    def set(self, key, value):
        """设置缓存项

        如果键已存在，会更新值并刷新过期时间
        如果缓存已满，会先清理过期项，然后再添加新项

        参数:
            key: 缓存键
            value: 缓存值
        """
        # 如果缓存已满，尝试清理过期项
        if len(self.cache) >= self.maxsize:
            self._clean_up()

        # 如果缓存仍然已满，移除最旧的项
        if len(self.cache) >= self.maxsize:
            self.cache.popitem(last=False)

        # 如果键已存在，移动到末尾（最新位置）
        if key in self.cache:
            self.cache.move_to_end(key)

        # 设置值和过期时间
        self.cache[key] = (value, time.time() + self.timeout)

    def get(self, key):
        """获取缓存项

        如果键存在且未过期，返回值并刷新访问顺序
        如果键不存在或已过期，返回None

        参数:
            key: 缓存键

        返回:
            缓存值或None（如果不存在或已过期）
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            # 检查是否过期
            if time.time() < expiry:
                # 刷新访问顺序
                self.cache.move_to_end(key)
                return value
            else:
                # 已过期，删除
                del self.cache[key]
        return None

    def delete(self, key):
        """删除缓存项

        参数:
            key: 要删除的缓存键
        """
        if key in self.cache:
            del self.cache[key]

    def _clean_up(self):
        """清理过期的缓存项"""
        current_time = time.time()
        # 找出所有过期的键
        expired_keys = [
            key
            for key, (_, expiry_time) in self.cache.items()
            if expiry_time <= current_time
        ]
        # 删除过期项
        for key in expired_keys:
            del self.cache[key]

    def __len__(self):
        """返回缓存中的项目数量"""
        return len(self.cache)


async def with_semaphore(semaphore, func, **kwargs):
    """在信号量控制下执行异步函数

    参数:
        semaphore: 用于控制并发的信号量对象
        func: 要执行的异步函数
        **kwargs: 传递给异步函数的关键字参数

    返回:
        异步函数的执行结果
    """
    try:
        async with semaphore:
            return await func(**kwargs)
    except Exception as e:
        logger.error(f"with_semaphore 执行异步函数{func.__name__}失败", e=e)
        return None
