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
    msg: str = ""
    """消息"""
    success: bool
    """是否成功"""

    def raise_for_code(self):
        if self.code != 200:
            raise APIResponseException(self.url or "", self.code, self.msg)
