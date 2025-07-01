from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class CallResult(BaseModel):
    code: int
    """错误码"""
    data: dict | str
    """数据"""
    is_success: bool = True
    """是否成功"""
