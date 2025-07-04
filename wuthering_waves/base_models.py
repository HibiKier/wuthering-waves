from typing import Generic, TypeVar

from pydantic import BaseModel

from .exceptions import APIResponseException

T = TypeVar("T")


class WwBaseResponse(BaseModel, Generic[T]):
    """库街区基础响应"""

    url: str | None = None
    """请求URL"""
    code: int
    """错误码"""
    data: T
    """数据"""
    msg: str | None = ""
    """消息"""
    success: bool
    """是否成功"""

    def __init__(self, **data):
        super().__init__(**data)
        self.raise_for_code()

    def raise_for_code(self):
        if self.code not in {10902, 200}:
            raise APIResponseException(self.url or "", self.code, self.msg)
