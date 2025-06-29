from tortoise import fields

from zhenxun.services.db_context import Model


class EmojiItem(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    emoji_id = fields.CharField(255, unique=True, description="表情的唯一标识ID")
    """表情的唯一标识ID"""
    img_url = fields.CharField(255, description="表情图片的URL地址")
    """表情图片的URL地址"""
    img_size = fields.CharField(255, description="表情图片的文件大小（字节）")
    """表情图片的文件大小（字节）"""
    name = fields.CharField(255, description="表情名称")
    """表情名称"""
    package_id = fields.CharField(255, description="所属表情包的ID")
    """所属表情包的ID"""
    is_downloaded = fields.BooleanField(default=False, description="是否已下载")
    """是否已下载"""
    path = fields.CharField(255, description="表情图片的本地路径")
    """表情图片的本地路径"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "emoji_items"
        table_description = "鸣潮表情项表"


class EmojiPackage(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    package_id = fields.CharField(255, unique=True, description="表情包唯一ID")
    """表情包唯一ID"""
    title = fields.CharField(255, description="表情包标题")
    """表情包标题"""
    creat_time = fields.DatetimeField(description="表情包创建时间")
    """表情包创建时间"""
    active_time = fields.DatetimeField(description="表情包生效时间")
    """表情包生效时间"""
    update_time = fields.DatetimeField(description="最后更新时间")
    """最后更新时间"""
    main_img_url = fields.CharField(255, description="表情包封面图URL")
    """表情包封面图URL"""
    state_code = fields.IntField(description="状态编码（1=未生效，2=生效中，3=已下架）")
    """状态编码（1=未生效，2=生效中，3=已下架）"""
    timing_active = fields.IntField(description="是否定时生效（0=否，1=是）")
    """是否定时生效（0=否，1=是）"""
    package_size = fields.CharField(255, description="表情包总大小（带单位）")
    """表情包总大小（带单位）"""
    state = fields.CharField(255, description="状态描述")
    """状态描述"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "emoji_packages"
        table_description = "鸣潮表情包表"
