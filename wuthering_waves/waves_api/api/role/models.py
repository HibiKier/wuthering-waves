from typing import Any

from pydantic import BaseModel, Field


class RoleInfo(BaseModel):
    """角色信息（这个是用户列表）模型"""

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


class RoleSkin(BaseModel):
    """角色皮肤信息"""

    is_addition: bool = Field(..., alias="isAddition", description="是否附加")
    """是否附加"""
    pic_url: str = Field(..., alias="picUrl", description="图片URL")
    """图片URL"""
    priority: int = Field(..., alias="priority", description="优先级")
    """优先级"""
    quality: int = Field(..., alias="quality", description="品质")
    """品质"""
    quality_name: str = Field(..., alias="qualityName", description="品质名称")
    """品质名称"""
    skin_icon: str = Field(..., alias="skinIcon", description="皮肤图标")
    """皮肤图标"""
    skin_id: int = Field(..., alias="skinId", description="皮肤ID")
    """皮肤ID"""
    skin_name: str = Field(..., alias="skinName", description="皮肤名称")
    """皮肤名称"""


class Role(BaseModel):
    """角色信息（这个是游戏内角色列表）"""

    acronym: str = Field(..., alias="acronym", description="首字母缩写")
    """首字母缩写"""
    attribute_id: int = Field(..., alias="attributeId", description="属性ID")
    """属性ID"""
    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    breach: int = Field(..., alias="breach", description="突破等级")
    """突破等级"""
    chain_unlock_num: int = Field(
        ..., alias="chainUnlockNum", description="链条解锁数量"
    )
    """链条解锁数量"""
    is_main_role: bool = Field(..., alias="isMainRole", description="是否主角")
    """是否主角"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""
    role_icon_url: str = Field(..., alias="roleIconUrl", description="角色图标URL")
    """角色图标URL"""
    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    role_pic_url: str = Field(..., alias="rolePicUrl", description="角色图片URL")
    """角色图片URL"""
    role_skin: RoleSkin = Field(..., alias="roleSkin", description="角色皮肤")
    """角色皮肤"""
    star_level: int = Field(..., alias="starLevel", description="星级")
    """星级"""
    total_skill_level: int = Field(
        ..., alias="totalSkillLevel", description="总技能等级"
    )
    """总技能等级"""
    weapon_type_id: int = Field(..., alias="weaponTypeId", description="武器类型ID")
    """武器类型ID"""
    weapon_type_name: str = Field(
        ..., alias="weaponTypeName", description="武器类型名称"
    )
    """武器类型名称"""


class RoleDataContent(BaseModel):
    """data字段的内部JSON内容"""

    role_list: list[Role] = Field(..., alias="roleList", description="角色列表")
    """角色列表"""
    show_to_guest: bool = Field(..., alias="showToGuest", description="是否对访客显示")
    """是否对访客显示"""


class Chain(BaseModel):
    """链条信息"""

    description: str = Field(..., alias="description", description="描述")
    """描述"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    order: int = Field(..., alias="order", description="顺序")
    """顺序"""
    unlocked: bool = Field(..., alias="unlocked", description="是否解锁")
    """是否解锁"""


class EquipPhantomAddProp(BaseModel):
    """装备声骸附加属性"""

    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""


class EquipPhantomAttribute(BaseModel):
    """装备声骸属性"""

    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    valid: bool = Field(..., alias="valid", description="是否有效")
    """是否有效"""


class PhantomProp(BaseModel):
    """声骸属性"""

    cost: int = Field(..., alias="cost", description="消耗")
    """消耗"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    phantom_id: int = Field(..., alias="phantomId", description="声骸ID")
    """声骸ID"""
    phantom_prop_id: int = Field(..., alias="phantomPropId", description="声骸属性ID")
    """声骸属性ID"""
    quality: int = Field(..., alias="quality", description="品质")
    """品质"""
    skill_description: str = Field(
        ..., alias="skillDescription", description="技能描述"
    )
    """技能描述"""


class FetterDetail(BaseModel):
    """羁绊详情"""

    first_description: str = Field(
        ..., alias="firstDescription", description="第一层描述"
    )
    """第一层描述"""
    group_id: int = Field(..., alias="groupId", description="组ID")
    """组ID"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    num: int = Field(..., alias="num", description="数量")
    """数量"""
    second_description: str = Field(
        ..., alias="secondDescription", description="第二层描述"
    )
    """第二层描述"""


class MainProp(BaseModel):
    """主属性"""

    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    valid: bool = Field(..., alias="valid", description="是否有效")
    """是否有效"""


class SubProp(BaseModel):
    """副属性"""

    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    valid: bool = Field(..., alias="valid", description="是否有效")
    """是否有效"""


class EquipPhantom(BaseModel):
    """装备声骸"""

    cost: int = Field(..., alias="cost", description="消耗")
    """消耗"""
    fetter_detail: FetterDetail = Field(
        ..., alias="fetterDetail", description="羁绊详情"
    )
    """羁绊详情"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""
    main_props: list[MainProp] = Field(..., alias="mainProps", description="主属性列表")
    """主属性列表"""
    phantom_prop: PhantomProp = Field(..., alias="phantomProp", description="声骸属性")
    """声骸属性"""
    quality: int = Field(..., alias="quality", description="品质")
    """品质"""
    sub_props: list[SubProp] = Field(..., alias="subProps", description="副属性列表")
    """副属性列表"""


class PhantomData(BaseModel):
    """声骸数据"""

    cost: int = Field(..., alias="cost", description="总消耗")
    """总消耗"""
    equip_phantom_list: list[EquipPhantom | None] = Field(
        default_factory=list, alias="equipPhantomList", description="装备声骸列表"
    )
    """装备声骸列表"""


class RoleBasicInfo(BaseModel):
    """角色基础信息（在 PhantomData 中引用）"""

    acronym: str = Field(..., alias="acronym", description="首字母缩写")
    """首字母缩写"""
    attribute_id: int = Field(..., alias="attributeId", description="属性ID")
    """属性ID"""
    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    breach: int = Field(..., alias="breach", description="突破等级")
    """突破等级"""
    chain_unlock_num: int = Field(
        ..., alias="chainUnlockNum", description="链条解锁数量"
    )
    """链条解锁数量"""
    is_main_role: bool | None = Field(
        None, alias="isMainRole", description="是否主角"
    )  # Optional because it's missing in this specific context
    """是否主角"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""
    role_icon_url: str = Field(..., alias="roleIconUrl", description="角色图标URL")
    """角色图标URL"""
    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    role_pic_url: str = Field(..., alias="rolePicUrl", description="角色图片URL")
    """角色图片URL"""
    star_level: int = Field(..., alias="starLevel", description="星级")
    """星级"""
    weapon_type_id: int = Field(..., alias="weaponTypeId", description="武器类型ID")
    """武器类型ID"""
    weapon_type_name: str = Field(
        ..., alias="weaponTypeName", description="武器类型名称"
    )
    """武器类型名称"""
    # role_skin is missing here in the "role" object, making it optional or omitted if not present


class RoleAttribute(BaseModel):
    """角色属性"""

    attribute_id: int = Field(..., alias="attributeId", description="属性ID")
    """属性ID"""
    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    sort: int = Field(..., alias="sort", description="排序")
    """排序"""


class RoleSkinFull(BaseModel):
    """完整的角色皮肤信息（在 RootModel.data.roleSkin 中引用）"""

    is_addition: bool = Field(..., alias="isAddition", description="是否附加")
    """是否附加"""
    pic_url: str = Field(..., alias="picUrl", description="图片URL")
    """图片URL"""
    priority: int = Field(..., alias="priority", description="优先级")
    """优先级"""
    quality: int = Field(..., alias="quality", description="品质")
    """品质"""
    quality_name: str = Field(..., alias="qualityName", description="品质名称")
    """品质名称"""
    skin_icon: str = Field(..., alias="skinIcon", description="皮肤图标")
    """皮肤图标"""
    skin_id: int = Field(..., alias="skinId", description="皮肤ID")
    """皮肤ID"""
    skin_name: str = Field(..., alias="skinName", description="皮肤名称")
    """皮肤名称"""


class Skill(BaseModel):
    """技能信息"""

    description: str = Field(..., alias="description", description="描述")
    """描述"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    id: int = Field(..., alias="id", description="ID")
    """ID"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    type: str = Field(..., alias="type", description="类型")
    """类型"""


class SkillItem(BaseModel):
    """技能列表项"""

    level: int = Field(..., alias="level", description="等级")
    """等级"""
    skill: Skill = Field(..., alias="skill", description="技能详情")
    """技能详情"""


class Weapon(BaseModel):
    """武器详情"""

    effect_description: str = Field(
        ..., alias="effectDescription", description="效果描述"
    )
    """效果描述"""
    weapon_effect_name: str = Field(
        ..., alias="weaponEffectName", description="武器效果名称"
    )
    """武器效果名称"""
    weapon_icon: str = Field(..., alias="weaponIcon", description="武器图标")
    """武器图标"""
    weapon_id: int = Field(..., alias="weaponId", description="武器ID")
    """武器ID"""
    weapon_name: str = Field(..., alias="weaponName", description="武器名称")
    """武器名称"""
    weapon_star_level: int = Field(..., alias="weaponStarLevel", description="武器星级")
    """武器星级"""
    weapon_type: int = Field(..., alias="weaponType", description="武器类型")
    """武器类型"""


class MainPropWeapon(BaseModel):
    """武器主属性"""

    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    attribute_value: str = Field(..., alias="attributeValue", description="属性值")
    """属性值"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""


class WeaponData(BaseModel):
    """武器数据"""

    breach: int = Field(..., alias="breach", description="突破等级")
    """突破等级"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""
    main_prop_list: list[MainPropWeapon] = Field(
        default_factory=list, alias="mainPropList", description="主属性列表"
    )
    """主属性列表"""
    reson_level: int = Field(..., alias="resonLevel", description="共鸣等级")
    """共鸣等级"""
    weapon: Weapon = Field(..., alias="weapon", description="武器详情")
    """武器详情"""


class CharDetailData(BaseModel):
    """data字段的内部JSON内容"""

    chain_list: list[Chain] = Field(
        default_factory=list, alias="chainList", description="链列表"
    )
    """链列表"""
    equip_phantom_add_prop_list: list[EquipPhantomAddProp] = Field(
        default_factory=list,
        alias="equipPhantomAddPropList",
        description="装备声骸附加属性列表",
    )
    """装备声骸附加属性列表"""
    equip_phantom_attribute_list: list[EquipPhantomAttribute] = Field(
        default_factory=list,
        alias="equipPhantomAttributeList",
        description="装备声骸属性列表",
    )
    """装备声骸属性列表"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""
    phantom_data: PhantomData = Field(..., alias="phantomData", description="声骸数据")
    """声骸数据"""
    role: RoleBasicInfo = Field(..., alias="role", description="角色基础信息")
    """角色基础信息"""
    role_attribute_list: list[RoleAttribute] = Field(
        default_factory=list, alias="roleAttributeList", description="角色属性列表"
    )
    """角色属性列表"""
    role_skin: RoleSkinFull = Field(..., alias="roleSkin", description="角色皮肤")
    """角色皮肤"""
    skill_list: list[SkillItem] = Field(
        default_factory=list, alias="skillList", description="技能列表"
    )
    """技能列表"""
    weapon_data: WeaponData = Field(..., alias="weaponData", description="武器数据")
    """武器数据"""


class SkillLevel(BaseModel):
    """技能等级信息"""

    type: str = Field(..., alias="type", description="技能类型")
    """技能类型"""
    level: int = Field(..., alias="level", description="等级")
    """等级"""


class RoleProgress(BaseModel):
    """角色进度信息项"""

    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    role_level: int = Field(..., alias="roleLevel", description="角色等级")
    """角色等级"""
    role_break_level: int = Field(
        ..., alias="roleBreakLevel", description="角色突破等级"
    )
    """角色突破等级"""
    skill_level_list: list[SkillLevel] = Field(
        ..., alias="skillLevelList", description="技能等级列表"
    )
    """技能等级列表"""
    skill_break_list: list[str] = Field(
        ..., alias="skillBreakList", description="技能突破列表"
    )
    """技能突破列表"""


class CostItem(BaseModel):
    """消耗物品项"""

    id: str = Field(..., alias="id", description="物品ID")
    """物品ID"""
    name: str = Field(..., alias="name", description="物品名称")
    """物品名称"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    num: int = Field(..., alias="num", description="数量")
    """数量"""
    type: int = Field(..., alias="type", description="类型")
    """类型"""
    quality: int = Field(..., alias="quality", description="品质")
    """品质"""
    is_preview: bool = Field(..., alias="isPreview", description="是否预览")
    """是否预览"""


class StrategyItem(BaseModel):
    """攻略项"""

    post_id: str = Field(..., alias="postId", description="帖子ID")
    """帖子ID"""
    post_title: str = Field(..., alias="postTitle", description="帖子标题")
    """帖子标题"""


class CostDetail(BaseModel):
    """消耗详情"""

    all_cost: list[CostItem] = Field(..., alias="allCost", description="所有消耗")
    """所有消耗"""
    missing_cost: list[CostItem] = Field(
        ..., alias="missingCost", description="缺失消耗"
    )
    """缺失消耗"""
    synthetic: list[CostItem] = Field(..., alias="synthetic", description="合成材料")
    """合成材料"""
    missing_role_cost: list[CostItem] | None = Field(
        ..., alias="missingRoleCost", description="缺失角色材料"
    )
    """缺失角色材料"""
    missing_skill_cost: list[CostItem] = Field(
        ..., alias="missingSkillCost", description="缺失技能材料"
    )
    """缺失技能材料"""
    missing_weapon_cost: Any | None = Field(
        ..., alias="missingWeaponCost", description="缺失武器材料"
    )  # null 或其他类型
    """缺失武器材料"""
    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    weapon_id: int | None = Field(
        ..., alias="weaponId", description="武器ID"
    )  # null 或其他类型
    """武器ID"""
    strategy_list: list[StrategyItem] = Field(
        ..., alias="strategyList", description="攻略列表"
    )
    """攻略列表"""
    show_strategy: bool = Field(..., alias="showStrategy", description="是否显示攻略")
    """是否显示攻略"""


class PreviewData(BaseModel):
    """预览数据"""

    all_cost: list[CostItem] = Field(..., alias="allCost", description="所有消耗")
    """所有消耗"""
    missing_cost: list[CostItem] = Field(
        ..., alias="missingCost", description="缺失消耗"
    )
    """缺失消耗"""
    synthetic: list[CostItem] = Field(..., alias="synthetic", description="合成材料")
    """合成材料"""
    missing_role_cost: list[CostItem] = Field(
        ..., alias="missingRoleCost", description="缺失角色材料"
    )
    """缺失角色材料"""
    missing_skill_cost: list[CostItem] = Field(
        ..., alias="missingSkillCost", description="缺失技能材料"
    )
    """缺失技能材料"""
    missing_weapon_cost: Any | None = Field(
        None, alias="missingWeaponCost", description="缺失武器材料"
    )  # null 或其他类型
    """缺失武器材料"""


class CostContent(BaseModel):
    """数据内容"""

    role_num: int = Field(..., alias="roleNum", description="角色数量")
    """角色数量"""
    weapon_num: int = Field(..., alias="weaponNum", description="武器数量")
    """武器数量"""
    preview: PreviewData = Field(..., alias="preview", description="预览数据")
    """预览数据"""
    cost_list: list[CostDetail] = Field(
        ..., alias="costList", description="消耗详情列表"
    )
    """消耗详情列表"""
