from typing import Literal, TypeVar, cast, overload

from tortoise import fields

from zhenxun.services.db_context import Model
from zhenxun.utils.common_utils import SqlUtils

from ..utils.emuns import CookieStatus

T = TypeVar("T", bound="WavesUser")


class WavesUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    cookie = fields.CharField(255, null=True, description="cookie")
    """cookie"""
    cookie_status = fields.CharEnumField(
        default=CookieStatus.NOT_LOGIN, enum_type=CookieStatus, description="cookie状态"
    )
    """cookie状态"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""
    role_id = fields.CharField(255, null=True, unique=True, description="鸣潮uid")
    """鸣潮uid"""
    waves_id = fields.CharField(255, null=True, description="鸣潮记录ID")
    """鸣潮id"""
    auto_sign = fields.BooleanField(default=False, description="是否自动签到")
    """是否自动签到"""
    access_token = fields.CharField(255, null=True, description="access_token")
    """access_token"""
    device_id = fields.CharField(255, null=True, description="设备id")
    """设备id"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_users"
        table_description = "鸣潮用户表"

    @classmethod
    async def expire_cookie(
        cls,
        *,
        cookie: str | None = None,
        user_id: str | None = None,
        role_id: str | None = None,
        waves_id: str | None = None,
    ):
        """失效cookie

        参数:
            cookie: 需要失效的cookie
            user_id: 需要失效的user_id
            role_id: 需要失效的role_id
        """
        if not user_id and not role_id and not cookie and not waves_id:
            raise ValueError("user_id, role_id, cookie, waves_id 不能同时为空")
        if user_id:
            await cls.filter(user_id=user_id).update(
                cookie_status=CookieStatus.LOGIN_INVALID
            )
        elif role_id:
            await cls.filter(role_id=role_id).update(
                cookie_status=CookieStatus.LOGIN_INVALID
            )
        elif cookie:
            await cls.filter(cookie=cookie).update(
                cookie_status=CookieStatus.LOGIN_INVALID
            )
        else:
            await cls.filter(waves_id=waves_id).update(
                cookie_status=CookieStatus.LOGIN_INVALID
            )

    @classmethod
    async def get_role_ids(cls, user_id: str) -> list[str]:
        """获取用户角色id"""
        return cast(
            list[str],
            await cls.filter(user_id=user_id).values_list("role_id", flat=True),
        )

    @classmethod
    async def get_waves_ids(cls, user_id: str) -> list[str]:
        """获取用户鸣潮uid"""
        return cast(
            list[str],
            await cls.filter(user_id=user_id).values_list("waves_id", flat=True),
        )

    @classmethod
    @overload
    async def random_cookie(
        cls, count: int = 1, *, only_cookie: Literal[False] = False
    ) -> list["WavesUser"]: ...

    @classmethod
    @overload
    async def random_cookie(
        cls, count: int = 1, *, only_cookie: Literal[True]
    ) -> list[tuple[str, str]]: ...

    @classmethod
    async def random_cookie(
        cls, count: int = 1, only_cookie: bool = False
    ) -> list[tuple[str, str]] | list["WavesUser"]:
        """随机获取一个登录成功的cookie

        参数:
            count: 获取数量
            only_cookie: 是否只返回cookie

        返回:
            list[tuple[str, str]] | list["WavesUser"]: 随机获取的用户或cookie列表
        """
        sql = SqlUtils.random(
            cls.filter(
                cookie__not_isnull=True, cookie_status=CookieStatus.LOGIN_SUCCESS
            ),
            count,
        )
        results: list["WavesUser"] = cast(list["WavesUser"], await cls.raw(sql))
        if only_cookie:
            return [(s.role_id, s.cookie) for s in results]
        else:
            return results

    @classmethod
    async def get_user_cookie(cls, role_id: str) -> "WavesUser | None":
        """获取指定角色id的cookie"""
        return await cls.get_or_none(role_id=role_id)

    @classmethod
    async def get_user_cookies(cls, user_id: str) -> list[dict[str, str]]:
        """获取用户所有cookie"""
        return await cls.filter(user_id=user_id).values("role_id", "cookie")
