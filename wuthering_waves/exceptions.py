from typing import Literal


class IPFetchFailedException(Exception):
    """所有IP获取方式都失败时抛出的异常"""

    def __init__(self, message: str = "所有IP获取方式均失败"):
        self.message = message
        super().__init__(self.message)


class APICallException(Exception):
    """API调用失败时抛出的异常"""

    def __init__(
        self,
        url: str | None,
        status_code: int | None = None,
        message: str | None = None,
    ):
        self.url = url
        self.status_code = status_code
        self.message = message or f"API '{url}' 调用失败"
        if status_code:
            self.message += f"，状态码: {status_code}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class APIResponseException(Exception):
    """API响应数据异常时抛出的异常

    当API调用成功（HTTP状态码正常），但响应数据中的业务状态码不为200时抛出
    """

    def __init__(
        self,
        url: str,
        code: int,
        message: str | None = None,
        data: dict | str | None = None,
    ):
        """初始化异常

        参数:
            url: API请求的URL
            code: 响应数据中的业务状态码
            message: 响应数据中的错误消息
            data: 响应数据中的其他数据
        """
        self.url = url
        self.code = code
        self.response_message = message  # 重命名避免与Exception的message冲突
        self.data = data

        # 构建异常消息
        error_msg = f"API '{url}' 业务异常"
        if code:
            error_msg += f"，业务状态码: {code}"
        if message:
            error_msg += f"，错误信息: {message}"

        super().__init__(error_msg)

    def __repr__(self) -> str:
        return super().__str__()

    def __str__(self) -> str:
        return f"请求失败，状态码: {self.code}\n消息: {self.response_message}"


class WavesException(Exception):
    """通用异常基类"""

    def __init__(self, message: str):
        """初始化异常

        参数:
            message: 错误消息
        """
        self.message: str = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class LoginStatusCheckException(Exception):
    """登录状态检查异常时抛出的异常"""

    def __init__(
        self,
        message: str | None = None,
        login_status: Literal["未绑定", "已过期", "未知异常", "参数错误", "调用异常"]
        | None = None,
    ):
        """初始化异常

        参数:
            message: 错误消息
            login_status: 登录状态
        """
        self.login_status = login_status
        self.message = message or "登录状态检查失败"

        # 构建详细的错误消息
        if login_status:
            self.message += f"，登录状态: {login_status}"

        super().__init__(self.message)

    def __str__(self):
        return f"[{self.login_status}]{self.message}"
