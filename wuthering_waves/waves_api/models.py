from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class CallResult(BaseModel):
    code: int
    """错误码"""
    data: dict | str
    """数据"""
    is_success: bool = True
    """是否成功"""


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


class RoleInfo(BaseModel):
    """角色信息模型"""

    id: int = Field(description="角色ID")
    """角色ID"""
    user_id: int = Field(..., alias="userId", description="用户ID")
    """用户ID"""
    game_id: int = Field(..., alias="gameId", description="游戏ID")
    """游戏ID"""
    server_id: str = Field(..., alias="serverId", description="服务器ID")
    """服务器ID"""
    server_name: str = Field(..., alias="serverName", description="服务器名称")
    """服务器名称"""
    role_id: str = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    is_default: bool = Field(..., alias="isDefault", description="是否为默认角色")
    """是否为默认角色"""
    game_head_url: str = Field(..., alias="gameHeadUrl", description="游戏头像URL")
    """游戏头像URL"""
    game_level: str = Field(..., alias="gameLevel", description="游戏等级")
    """游戏等级"""
    role_score: float | None = Field(None, alias="roleScore", description="角色评分")
    """角色评分"""
    role_num: int = Field(..., alias="roleNum", description="角色数量")
    """角色数量"""
    fashion_collection_percent: int = Field(
        ..., alias="fashionCollectionPercent", description="时装收集百分比"
    )
    """时装收集百分比"""
    phantom_percent: int = Field(..., alias="phantomPercent", description="幻影百分比")
    """幻影百分比"""
    achievement_count: int = Field(
        ..., alias="achievementCount", description="成就数量"
    )
    """成就数量"""
    action_recover_switch: bool = Field(
        ..., alias="actionRecoverSwitch", description="行动恢复开关"
    )
    """行动恢复开关"""
    widget_has_pull: bool = Field(
        ..., alias="widgetHasPull", description="小组件是否有拉取"
    )
    """小组件是否有拉取"""
    point_after: str | None = Field(None, alias="pointAfter", description="后续点数")
    """后续点数"""


class RequestToken(BaseModel):
    """请求token结果"""

    access_token: str = Field(..., alias="accessToken", description="access_token")
    """access_token"""
