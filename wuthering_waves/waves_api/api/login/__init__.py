from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar, TypeVar

from zhenxun.utils.platform import PlatformUtils

from ....base_models import WwBaseResponse
from ....exceptions import LoginStatusCheckException, WavesException
from ....models.waves_user import WavesUser
from ....utils.utils import TimedCache
from ...const import (
    LOGIN_H5_URL,
    LOGIN_LOG_URL,
    LOGIN_URL,
    REFRESH_URL,
    REQUEST_TOKEN,
    SUCCESS_CODE,
)
from ...error_code import ERROR_CODE, WAVES_CODE_998
from ...headers import KURO_VERSION, get_headers
from ..call import CallApi, get_server_id, login_platform
from .models import LoginResult, RequestToken

F = TypeVar("F", bound=Callable[..., Any])


time_cache = TimedCache()


def login_status_check(role_id_param: str = "role_id"):
    """登录状态检查装饰器

    用于装饰需要检查登录状态的API调用方法

    参数:
        role_id_param: 角色ID参数名，默认为 "role_id"

    使用示例:
        @login_status_check("role_id")
        async def some_api_call(cls, role_id: str, **kwargs):
            # API调用逻辑
            pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取角色ID
            role_id = kwargs.get(role_id_param)

            if not role_id:
                return await func(*args, **kwargs)

            # 生成缓存键
            cache_key = f"{role_id}"

            # 检查缓存
            cached_result = time_cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            try:
                # 执行原始函数
                result = await func(*args, **kwargs)

                # 如果返回的是响应对象，进行登录状态检查
                if hasattr(result, "code") and hasattr(result, "msg"):
                    await LoginApi.login_check(role_id, result)

                # 更新缓存，使用默认的60秒过期时间
                time_cache.set(cache_key, result)

                return result

            except LoginStatusCheckException:
                # 重新抛出登录状态检查异常
                raise
            except Exception as e:
                # 其他异常包装为登录状态检查异常
                raise WavesException(f"API调用失败: {e!s}") from e

        return wrapper  # type: ignore

    return decorator


class LoginApi:
    _bat_cache: ClassVar[dict[str, str]] = {}

    @classmethod
    async def login(
        cls, mobile: str, code: str, device_id: str
    ) -> WwBaseResponse[LoginResult]:
        """登录

        参数:
            mobile: 手机号
            code: 验证码
            device_id: 设备id

        返回:
            CallResult: 登录结果
        """
        platform = login_platform()
        header = await get_headers(platform=platform)
        data = {
            "mobile": mobile,
            "code": code,
            "devCode": device_id,
        }
        url = LOGIN_H5_URL if platform == "h5" else LOGIN_URL
        response = await CallApi.call_post(url, header=header, data=data)
        # 兼容pydantic 1.x
        response.data = LoginResult(**response.data)
        return response

    @classmethod
    async def request_token(
        cls, role_id: str, cookie: str, device_id: str, server_id: str | None = None
    ) -> WwBaseResponse[RequestToken]:
        """获取access_token

        参数:
            role_id: 角色id
            token: 登录token
            device_id: 设备id
            server_id: 服务器id

        返回:
            WwBaseResponse[RequestToken]: 获取access_token
        """
        header = await get_headers(cookie, role_id=role_id)
        header.update({"token": cookie, "did": device_id, "b-at": ""})
        response = await CallApi.call_post(
            REQUEST_TOKEN,
            header=header,
            data={
                "serverId": server_id or get_server_id(role_id),
                "roleId": role_id,
            },
        )
        # 兼容pydantic 1.x
        response.data = RequestToken(**response.data)
        return response

    @classmethod
    async def login_check(cls, role_id: str, response: WwBaseResponse):
        """登录状态检查

        参数:
            role_id: 角色id
            response: 响应数据

        异常:
            LoginStatusCheckException: 登录状态检查异常
        """
        if response.code in SUCCESS_CODE:
            return
        message = response.msg or ""
        if message in {"请求成功", "系统繁忙，请稍后再试"}:
            raise LoginStatusCheckException(
                f"鸣潮账号id: 【{role_id}】未绑定库街区!!!\n"
                "1.是否注册过库街区\n2.库街区能否查询当前鸣潮账号数据",
                login_status="未绑定",
            )
        if "重新登录" in message or "登录已过期" in message:
            await WavesUser.expire_cookie(role_id=role_id)
            raise LoginStatusCheckException(
                f"鸣潮账号id: 【{role_id}】登录已过期!!!",
                login_status="已过期",
            )

        if "访问被阻断" in message:
            await PlatformUtils.send_superuser(None, ERROR_CODE[WAVES_CODE_998])

        if isinstance(response.data, str) and (
            "RABC" in response.data or "access denied" in response.data
        ):
            await PlatformUtils.send_superuser(None, ERROR_CODE[WAVES_CODE_998])

        if message:
            await PlatformUtils.send_superuser(None, message)
        raise LoginStatusCheckException(
            f"鸣潮账号id: 【{role_id}】登录状态异常!!!\n{message}",
            login_status="未知异常",
        )

    @classmethod
    @login_status_check()
    async def login_log(cls, role_id: str, cookie: str) -> WwBaseResponse[bool]:
        """登录状态检查

        参数:
            rold_id: 角色id
            token: 令牌

        返回:
            WwBaseResponse[bool]: 登录状态检查
        """
        header = await get_headers(cookie, role_id=role_id)
        header.update(
            {
                "token": cookie,
                "devCode": header.get("did", ""),
                "version": KURO_VERSION,
            }
        )
        header.pop("did", None)
        header.pop("b-at", None)
        response = await CallApi.call_post(LOGIN_LOG_URL, header=header)
        return response

    @classmethod
    @login_status_check()
    async def refresh(
        cls, role_id: str, cookie: str, server_id: str | None = None
    ) -> WwBaseResponse[bool]:
        """刷新登录状态

        参数:
            role_id: 角色id
            cookie: 登录token
            server_id: 服务器id

        返回:
            WwBaseResponse[bool]: 刷新结果
        """
        header = await get_headers(cookie, role_id=role_id)

        return await CallApi.call_post(
            REFRESH_URL,
            headers=header,
            data=CallApi.default_params(role_id, server_id),
        )
