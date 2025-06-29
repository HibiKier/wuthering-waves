import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum


class CookieStatus(StrEnum):
    """cookie状态"""

    NOT_LOGIN = "NOT_LOGIN"
    """未登录"""
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    """登录成功"""
    LOGIN_INVALID = "LOGIN_INVALID"
    """登录失效"""
