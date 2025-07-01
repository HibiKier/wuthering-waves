from pydantic import BaseModel, Field


class LoginResult(BaseModel):
    """登录结果"""

    enable_child_mode: bool = Field(
        ..., alias="enableChildMode", description="是否开启儿童模式"
    )
    """是否开启儿童模式"""
    gender: int = Field(..., description="性别")
    """性别"""
    head_url: str = Field(..., alias="headUrl", description="头像")
    """头像"""
    is_admin: bool = Field(..., alias="isAdmin", description="是否为管理员")
    """是否为管理员"""
    is_register: int = Field(..., alias="isRegister", description="是否注册")
    """是否注册"""
    signature: str = Field(..., description="个性签名")
    """个性签名"""
    token: str = Field(..., description="token")
    """token"""
    user_id: int = Field(..., alias="userId", description="用户ID")
    """用户ID"""
    user_name: str = Field(..., alias="userName", description="用户名")
    """用户名"""


class RequestToken(BaseModel):
    """请求token结果"""

    access_token: str = Field(..., alias="accessToken", description="access_token")
    """access_token"""
