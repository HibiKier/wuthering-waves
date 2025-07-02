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

    role_list: list[Role] = Field(..., alias="rolelist", description="角色列表")
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
    equip_phantom_list: list[EquipPhantom] = Field(
        default_factory=list, alias="equipPhantomlist", description="装备声骸列表"
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
        default_factory=list, alias="mainProplist", description="主属性列表"
    )
    """主属性列表"""
    reson_level: int = Field(..., alias="resonLevel", description="共鸣等级")
    """共鸣等级"""
    weapon: Weapon = Field(..., alias="weapon", description="武器详情")
    """武器详情"""


class CharDetailData(BaseModel):
    """data字段的内部JSON内容"""

    chain_list: list[Chain] = Field(
        default_factory=list, alias="chainlist", description="链列表"
    )
    """链列表"""
    equip_phantom_add_prop_list: list[EquipPhantomAddProp] = Field(
        default_factory=list,
        alias="equipPhantomAddProplist",
        description="装备声骸附加属性列表",
    )
    """装备声骸附加属性列表"""
    equip_phantom_attribute_list: list[EquipPhantomAttribute] = Field(
        default_factory=list,
        alias="equipPhantomAttributelist",
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
        default_factory=list, alias="roleAttributelist", description="角色属性列表"
    )
    """角色属性列表"""
    role_skin: RoleSkinFull = Field(..., alias="roleSkin", description="角色皮肤")
    """角色皮肤"""
    skill_list: list[SkillItem] = Field(
        default_factory=list, alias="skilllist", description="技能列表"
    )
    """技能列表"""
    weapon_data: WeaponData = Field(..., alias="weaponData", description="武器数据")
    """武器数据"""


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
