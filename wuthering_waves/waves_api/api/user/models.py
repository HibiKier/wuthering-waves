from pydantic import BaseModel, Field


class BoxItem(BaseModel):
    box_name: str = Field(..., alias="boxName", description="箱子名称")
    """箱子名称"""
    num: int = Field(..., description="箱子数量")
    """箱子数量"""


class PhantomBoxItem(BaseModel):
    name: str = Field(..., description="幻痛箱名称")
    """潮汐之遗名称"""
    num: int = Field(..., description="幻痛箱数量")
    """潮汐之遗数量"""


class TreasureBoxItem(BaseModel):
    name: str = Field(..., description="宝藏箱名称")
    """已收集宝藏箱名称"""
    num: int = Field(..., description="宝藏箱数量")
    """已收集宝藏箱数量"""


class BaseUserData(BaseModel):
    achievement_count: int = Field(
        ..., alias="achievementCount", description="成就数量"
    )
    """成就数量"""
    achievement_star: int = Field(..., alias="achievementStar", description="成就星星")
    """成就星星"""
    active_days: int = Field(..., alias="activeDays", description="活跃天数")
    """活跃天数"""
    big_count: int = Field(..., alias="bigCount", description="大数量")
    """大数量"""
    box_list: list[BoxItem] = Field(..., alias="boxList", description="箱子列表")
    """箱子列表"""
    chapter_id: int = Field(..., alias="chapterId", description="章节ID")
    """章节ID"""
    creat_time: int = Field(..., alias="creatTime", description="创建时间戳")
    """创建时间戳"""
    energy: int = Field(..., description="当前能量")
    """当前能量"""
    id: int = Field(..., description="用户ID")
    """用户ID"""
    level: int = Field(..., description="等级")
    """等级"""
    liveness: int = Field(..., description="活跃度")
    """活跃度"""
    liveness_max_count: int = Field(
        ..., alias="livenessMaxCount", description="最大活跃度"
    )
    """最大活跃度"""
    liveness_unlock: bool = Field(
        ..., alias="livenessUnlock", description="活跃度是否解锁"
    )
    """活跃度是否解锁"""
    max_energy: int = Field(..., alias="maxEnergy", description="最大能量")
    """最大能量"""
    name: str = Field(..., description="用户名")
    """用户名"""
    phantom_box_list: list[PhantomBoxItem] = Field(
        ..., alias="phantomBoxList", description="幻痛箱列表"
    )
    """幻痛箱列表"""
    role_num: int = Field(..., alias="roleNum", description="角色数量")
    """角色数量"""
    rouge_icon_url: str | None = Field(
        None, alias="rougeIconUrl", description="红图标URL"
    )
    """千道门扉的异想图标URL"""
    rouge_score: int | None = Field(
        None, alias="rougeScore", description="千道门扉的异想"
    )
    """千道门扉的异想"""
    rouge_score_limit: int | None = Field(
        None, alias="rougeScoreLimit", description="千道门扉的异想限制"
    )
    """千道门扉的异想限制"""
    rouge_title: str | None = Field(
        None, alias="rougeTitle", description="千道门扉的异想标题"
    )
    """千道门扉的异想标题"""
    show_birth_icon: bool = Field(
        ..., alias="showBirthIcon", description="是否显示生日图标"
    )
    """是否显示生日图标"""
    show_to_guest: bool = Field(..., alias="showToGuest", description="是否对访客显示")
    """是否对访客显示"""
    small_count: int = Field(..., alias="smallCount", description="小数量")
    """小数量"""
    store_energy: int = Field(..., alias="storeEnergy", description="存储能量")
    """存储能量"""
    store_energy_icon_url: str = Field(
        ..., alias="storeEnergyIconUrl", description="存储能量图标URL"
    )
    """存储能量图标URL"""
    store_energy_limit: int = Field(
        ..., alias="storeEnergyLimit", description="存储能量限制"
    )
    """存储能量限制"""
    store_energy_title: str = Field(
        ..., alias="storeEnergyTitle", description="存储能量标题"
    )
    """存储能量标题"""
    treasure_box_list: list[TreasureBoxItem] = Field(
        ..., alias="treasureBoxList", description="宝藏箱列表"
    )
    """宝藏箱列表"""
    weekly_inst_count: int = Field(
        ..., alias="weeklyInstCount", description="每周实例计数"
    )
    """每周实例计数"""
    weekly_inst_count_limit: int = Field(
        ..., alias="weeklyInstCountLimit", description="每周实例计数限制"
    )
    """每周实例计数限制"""
    weekly_inst_icon_url: str = Field(
        ..., alias="weeklyInstIconUrl", description="每周实例图标URL"
    )
    """每周实例图标URL"""
    weekly_inst_title: str = Field(
        ..., alias="weeklyInstTitle", description="每周实例标题"
    )
    """每周实例标题"""
    world_level: int = Field(..., alias="worldLevel", description="世界等级")
    """世界等级"""


class RoleSkin(BaseModel):
    is_addition: bool = Field(..., alias="isAddition", description="是否为附加皮肤")
    """是否为附加皮肤"""
    pic_url: str = Field(..., alias="picUrl", description="皮肤图片URL")
    """皮肤图片URL"""
    priority: int = Field(..., description="优先级")
    """优先级"""
    quality: int = Field(..., description="品质等级")
    """品质等级"""
    quality_name: str = Field(..., alias="qualityName", description="品质名称")
    """品质名称"""
    skin_icon: str = Field(..., alias="skinIcon", description="皮肤图标URL")
    """皮肤图标URL"""
    skin_id: int = Field(..., alias="skinId", description="皮肤ID")
    """皮肤ID"""
    skin_name: str = Field(..., alias="skinName", description="皮肤名称")
    """皮肤名称"""


class RoleInfo(BaseModel):
    acronym: str = Field(..., description="角色缩写")
    """角色缩写"""
    attribute_id: int = Field(..., alias="attributeId", description="属性ID")
    """属性ID"""
    attribute_name: str = Field(..., alias="attributeName", description="属性名称")
    """属性名称"""
    breach: int = Field(..., description="突破等级")
    """突破等级"""
    chain_unlock_num: int = Field(
        ..., alias="chainUnlockNum", description="连锁解锁数量"
    )
    """连锁解锁数量"""
    is_main_role: bool = Field(..., alias="isMainRole", description="是否为主角色")
    """是否为主角色"""
    level: int = Field(..., description="角色等级")
    """角色等级"""
    role_icon_url: str = Field(..., alias="roleIconUrl", description="角色图标URL")
    """角色图标URL"""
    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""
    role_name: str = Field(..., alias="roleName", description="角色名称")
    """角色名称"""
    role_pic_url: str = Field(..., alias="rolePicUrl", description="角色图片URL")
    """角色图片URL"""
    role_skin: RoleSkin = Field(..., alias="roleSkin", description="角色皮肤信息")
    """角色皮肤信息"""
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


class RoleListData(BaseModel):
    role_list: list[RoleInfo] = Field(..., alias="roleList", description="角色列表")
    """角色列表"""
    show_to_guest: bool = Field(..., alias="showToGuest", description="是否对访客显示")
    """是否对访客显示"""
    show_role_id_list: list[int] | None = Field(
        None, alias="showRoleIdList", description="显示角色ID列表"
    )
    """显示角色ID列表"""


class TowerRoleInfo(BaseModel):
    icon_url: str = Field(..., alias="iconUrl", description="角色图标URL")
    """角色图标URL"""
    role_id: int = Field(..., alias="roleId", description="角色ID")
    """角色ID"""


class FloorInfo(BaseModel):
    floor: int = Field(..., description="楼层编号")
    """楼层编号"""
    pic_url: str = Field(..., alias="picUrl", description="楼层图片URL")
    """楼层图片URL"""
    role_list: list[TowerRoleInfo] | None = Field(
        None, alias="roleList", description="角色列表"
    )
    """角色列表"""
    star: int = Field(..., description="获得星数")
    """获得星数"""


class TowerAreaInfo(BaseModel):
    area_id: int = Field(..., alias="areaId", description="区域ID")
    """区域ID"""
    area_name: str = Field(..., alias="areaName", description="区域名称")
    """区域名称"""
    floor_list: list[FloorInfo] = Field(..., alias="floorList", description="层级列表")
    """层级列表"""
    max_star: int = Field(..., alias="maxStar", description="最大星数")
    """最大星数"""
    star: int = Field(..., description="当前星数")
    """当前星数"""


class DifficultyInfo(BaseModel):
    difficulty: int = Field(..., description="难度级别")
    """难度级别"""
    difficulty_name: str = Field(..., alias="difficultyName", description="难度名称")
    """难度名称"""
    tower_area_list: list[TowerAreaInfo] = Field(
        ..., alias="towerAreaList", description="塔区域列表"
    )
    """塔区域列表"""


class TowerData(BaseModel):
    difficulty_list: list[DifficultyInfo] = Field(
        ..., alias="difficultyList", description="难度列表"
    )
    """难度列表"""
    is_unlock: bool = Field(..., alias="isUnlock", description="是否已解锁")
    """是否已解锁"""
    season_end_time: int = Field(..., alias="seasonEndTime", description="结束时间戳")
    """结束时间戳"""
