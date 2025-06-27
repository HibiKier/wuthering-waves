class IPFetchFailedException(Exception):
    """所有IP获取方式都失败时抛出的异常"""

    def __init__(self, message: str = "所有IP获取方式均失败"):
        self.message = message
        super().__init__(self.message)


class APICallException(Exception):
    """API调用失败时抛出的异常"""

    def __init__(
        self,
        url: str,
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
