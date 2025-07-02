from tortoise import fields

from zhenxun.services.db_context import Model


def get_model_ref(model_name: str) -> str:
    """动态生成模型引用字符串"""
    return f"models.{model_name}"


class Role(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    role_id = fields.IntField(description="角色ID")
    level = fields.IntField(description="角色等级")
    breach = fields.IntField(null=True, description="突破等级")
    role_name = fields.CharField(255, description="角色名称")
    role_icon_url = fields.CharField(255, null=True, description="角色头像")
    role_pic_url = fields.CharField(255, null=True, description="角色立绘")
    star_level = fields.IntField(description="星级")
    attribute_id = fields.IntField(description="属性ID")
    attribute_name = fields.CharField(255, null=True, description="属性名称")
    weapon_type_id = fields.IntField(description="武器类型ID")
    weapon_type_name = fields.CharField(255, null=True, description="武器类型")
    acronym = fields.CharField(255, description="简称")
    chain_unlock_num = fields.IntField(null=True, description="解锁链数")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "roles"
        table_description = "角色详细信息表"


class Skill(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    skill_id = fields.IntField(unique=True, description="技能ID")
    type = fields.CharField(50, description="技能类型")
    name = fields.CharField(255, description="技能名称")
    description = fields.TextField(description="技能描述")
    icon_url = fields.CharField(255, description="技能图标")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "skill"
        table_description = "技能表"


class Chain(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    name = fields.CharField(255, null=True, description="链名称")
    order = fields.IntField(description="顺序")
    description = fields.TextField(null=True, description="描述")
    icon_url = fields.CharField(255, null=True, description="图标")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "chain"
        table_description = "角色链表"


class WeaponDetail(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    weapon_id = fields.IntField(unique=True, description="武器ID")
    weapon_name = fields.CharField(255, description="武器名称")
    weapon_type = fields.IntField(description="武器类型")
    weapon_star_level = fields.IntField(description="武器星级")
    weapon_icon = fields.CharField(255, null=True, description="武器图标")
    weapon_effect_name = fields.CharField(255, null=True, description="武器效果名称")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "weapon_detail"
        table_description = "武器表"


class Weapon(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    role = fields.ForeignKeyField(get_model_ref("Role"), related_name="weapon")
    weapon_detail = fields.ForeignKeyField(
        get_model_ref("WeaponDetail"), related_name="weapon"
    )
    level = fields.IntField(description="武器等级")
    breach = fields.IntField(null=True, description="武器突破等级")
    reson_level = fields.IntField(null=True, description="共鸣等级")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "weapons"
        table_description = "武器数据表"


class FetterDetail(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    group_id = fields.IntField(description="羁绊组ID")
    name = fields.CharField(255, description="羁绊名称")
    icon_url = fields.CharField(255, null=True, description="羁绊图标")
    num = fields.IntField(description="羁绊数量")
    first_description = fields.TextField(null=True, description="第一段描述")
    second_description = fields.TextField(null=True, description="第二段描述")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "fetter_detail"
        table_description = "羁绊详情表"


class Props(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    attribute_name = fields.CharField(255, description="属性名称")
    icon_url = fields.CharField(255, null=True, description="属性图标")
    attribute_value = fields.CharField(255, description="属性值")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "props"
        table_description = "属性表"


class Phantom(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    role = fields.ForeignKeyField(get_model_ref("Role"), related_name="phantoms")
    cost = fields.IntField(description="消耗")
    quality = fields.IntField(description="品质")
    level = fields.IntField(description="等级")
    fetter_detail = fields.ForeignKeyField(
        get_model_ref("FetterDetail"), related_name="phantoms"
    )

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "phantom"
        table_description = "声骇装备表"


class PhantomProps(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    phantom = fields.ForeignKeyField(
        get_model_ref("Phantom"), related_name="phantom_props"
    )
    props = fields.ForeignKeyField(get_model_ref("Props"), related_name="phantom_props")
    is_main = fields.BooleanField(description="是否主属性")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "phantom_props"
        table_description = "声骇装备属性关联表"
