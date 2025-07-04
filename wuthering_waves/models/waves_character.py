from typing import TYPE_CHECKING, cast

from tortoise import fields

from zhenxun.services.db_context import Model

if TYPE_CHECKING:
    from .waves_character import WavesWeapon


def get_model_ref(model_name: str) -> str:
    """动态生成模型引用字符串"""
    return f"models.{model_name}"


class WavesCharacterBase(Model):
    """角色基础信息表，存储角色固有属性"""

    char_id = fields.IntField(pk=True, description="角色ID")
    char_name = fields.CharField(255, description="角色名称")
    char_icon_url = fields.CharField(255, null=True, description="角色头像")
    char_pic_url = fields.CharField(255, null=True, description="角色立绘")
    star_level = fields.IntField(description="星级")
    attribute_id = fields.IntField(description="属性ID")
    attribute_name = fields.CharField(255, null=True, description="属性名称")
    weapon_type_id = fields.IntField(description="武器类型ID")
    weapon_type_name = fields.CharField(255, null=True, description="武器类型")
    acronym = fields.CharField(255, description="简称")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_character_base"
        table_description = "角色基础信息表"


class WavesCharacter(Model):
    """角色用户数据表，存储用户特定的角色数据"""

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    role_id = fields.CharField(255, description="角色（用户）ID")
    character_base = fields.ForeignKeyField(
        get_model_ref("WavesCharacterBase"), related_name="characters"
    )
    level = fields.IntField(description="角色等级")
    breach = fields.IntField(null=True, description="突破等级")
    chain_unlock_num = fields.IntField(null=True, description="解锁链数")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_characters"
        table_description = "角色用户数据表"
        unique_together = ("role_id", "character_base")

    @classmethod
    async def get_chars(cls, role_id: str) -> list["WavesCharacter"]:
        """获取角色列表"""
        return cast(
            list["WavesCharacter"],
            await cls.filter(role_id=role_id).prefetch_related("character_base").all(),
        )

    @classmethod
    async def get_chars_with_weapons(cls, role_id: str) -> list["WavesCharacter"]:
        """获取角色列表及其武器信息"""
        return cast(
            list["WavesCharacter"],
            await cls.filter(role_id=role_id)
            .prefetch_related("character_base", "weapon__weapon_detail")
            .all(),
        )


class WavesSkill(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    skill_id = fields.IntField(unique=True, description="技能ID")
    type = fields.CharField(50, description="技能类型")
    name = fields.CharField(255, description="技能名称")
    description = fields.TextField(description="技能描述")
    icon_url = fields.CharField(255, description="技能图标")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_skills"
        table_description = "技能表"


class WavesChain(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    character_base = fields.ForeignKeyField(
        get_model_ref("WavesCharacterBase"), related_name="chains"
    )
    name = fields.CharField(255, null=True, description="链名称")
    order = fields.IntField(description="顺序")
    description = fields.TextField(null=True, description="描述")
    icon_url = fields.CharField(255, null=True, description="图标")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_chains"
        table_description = "角色链表"


class WavesWeaponDetail(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    weapon_id = fields.IntField(unique=True, description="武器ID")
    weapon_name = fields.CharField(255, description="武器名称")
    weapon_type = fields.IntField(description="武器类型")
    weapon_star_level = fields.IntField(description="武器星级")
    weapon_icon = fields.CharField(255, null=True, description="武器图标")
    weapon_effect_name = fields.CharField(255, null=True, description="武器效果名称")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_weapon_details"
        table_description = "武器表"


class WavesWeapon(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    character = fields.ForeignKeyField(
        get_model_ref("WavesCharacter"), related_name="weapon"
    )
    weapon_detail = fields.ForeignKeyField(
        get_model_ref("WavesWeaponDetail"), related_name="weapon"
    )
    level = fields.IntField(description="武器等级")
    breach = fields.IntField(null=True, description="武器突破等级")
    reson_level = fields.IntField(null=True, description="共鸣等级")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_weapons"
        table_description = "武器数据表"


class WavesFetterDetail(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    group_id = fields.IntField(description="羁绊组ID")
    name = fields.CharField(255, description="羁绊名称")
    icon_url = fields.CharField(255, null=True, description="羁绊图标")
    num = fields.IntField(description="羁绊数量")
    first_description = fields.TextField(null=True, description="第一段描述")
    second_description = fields.TextField(null=True, description="第二段描述")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_fetter_details"
        table_description = "羁绊详情表"


class WavesProps(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    attribute_name = fields.CharField(255, description="属性名称")
    icon_url = fields.CharField(255, null=True, description="属性图标")
    attribute_value = fields.CharField(255, description="属性值")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_props"
        table_description = "属性表"


class WavesPhantom(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    character = fields.ForeignKeyField(
        get_model_ref("WavesCharacter"), related_name="phantoms"
    )
    cost = fields.IntField(description="消耗")
    quality = fields.IntField(description="品质")
    level = fields.IntField(description="等级")
    fetter_detail = fields.ForeignKeyField(
        get_model_ref("WavesFetterDetail"), related_name="phantoms"
    )

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_phantoms"
        table_description = "声骇装备表"


class WavesPhantomProps(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    phantom = fields.ForeignKeyField(
        get_model_ref("WavesPhantom"), related_name="phantom_props"
    )
    props = fields.ForeignKeyField(
        get_model_ref("WavesProps"), related_name="phantom_props"
    )
    is_main = fields.BooleanField(description="是否主属性")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_phantom_props"
        table_description = "声骇装备属性关联表"


# 修改WavesCharacter与Skill的关联表
class WavesCharSkill(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    character = fields.ForeignKeyField(
        get_model_ref("WavesCharacter"), related_name="char_skills"
    )
    skill = fields.ForeignKeyField(
        get_model_ref("WavesSkill"), related_name="char_skills"
    )
    level = fields.IntField(description="技能等级")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_char_skills"
        table_description = "角色技能关联表"
        unique_together = ("character", "skill")


# 修改WavesCharacter与Chain的关联表
class WavesCharChain(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    character = fields.ForeignKeyField(
        get_model_ref("WavesCharacter"), related_name="char_chains"
    )
    chain = fields.ForeignKeyField(
        get_model_ref("WavesChain"), related_name="char_chains"
    )
    is_unlocked = fields.BooleanField(default=False, description="是否解锁")

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_char_chains"
        table_description = "角色链解锁关联表"
        unique_together = ("character", "chain")
