from pydantic import BaseModel, Field


class CommonSkill(BaseModel):
    """通用技能信息"""

    type: str = Field(..., alias="type", description="技能类型")
    """技能类型"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""


class AdvanceSkill(BaseModel):
    """进阶技能信息"""

    location: str = Field(..., alias="location", description="技能位置")
    """技能位置"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""


class RoleItem(BaseModel):
    """角色列表项"""

    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    role_icon_url: str = Field(..., alias="roleIconUrl", description="角色图标URL")
    """角色图标URL"""
    star_level: int = Field(..., alias="starLevel", description="星级")
    """星级"""
    attribute_id: int = Field(..., alias="attributeId", description="属性ID")
    """属性ID"""
    attribute_name: str | None = Field(
        None, alias="attributeName", description="属性名称"
    )
    """属性名称"""
    weapon_type_id: int = Field(..., alias="weaponTypeId", description="武器类型ID")
    """武器类型ID"""
    weapon_type_name: str = Field(
        ..., alias="weaponTypeName", description="武器类型名称"
    )
    """武器类型名称"""
    acronym: str = Field(..., alias="acronym", description="首字母缩写")
    """首字母缩写"""
    is_preview: bool = Field(..., alias="isPreview", description="是否预览")
    """是否预览"""
    is_new: bool = Field(..., alias="isNew", description="是否新角色")
    """是否新角色"""
    priority: int = Field(..., alias="priority", description="优先级")
    """优先级"""
    common_skill_list: list[CommonSkill] = Field(
        ..., alias="commonSkillList", description="通用技能列表"
    )
    """通用技能列表"""
    advance_skill_list: list[AdvanceSkill] = Field(
        ..., alias="advanceSkillList", description="进阶技能列表"
    )
    """进阶技能列表"""


class WeaponItem(BaseModel):
    """武器信息项"""

    weapon_id: int = Field(..., alias="weaponId", description="武器ID")
    """武器ID"""
    weapon_name: str = Field(..., alias="weaponName", description="武器名称")
    """武器名称"""
    weapon_type: int = Field(..., alias="weaponType", description="武器类型")
    """武器类型"""
    weapon_star_level: int = Field(..., alias="weaponStarLevel", description="武器星级")
    """武器星级"""
    weapon_icon: str = Field(..., alias="weaponIcon", description="武器图标URL")
    """武器图标URL"""
    is_preview: bool = Field(..., alias="isPreview", description="是否预览")
    """是否预览"""
    is_new: bool = Field(..., alias="isNew", description="是否新武器")
    """是否新武器"""
    priority: int = Field(..., alias="priority", description="优先级")
    """优先级"""
    acronym: str = Field(..., alias="acronym", description="首字母缩写")
    """首字母缩写"""
