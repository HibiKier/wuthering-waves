from tortoise import fields

from zhenxun.services.db_context import Model


class WavesUser(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    cookie = fields.CharField(255, null=True, description="cookie")
    """cookie"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""
    role_id = fields.CharField(255, null=True, unique=True, description="鸣潮uid")
    """鸣潮uid"""
    record_id = fields.CharField(255, null=True, description="鸣潮记录ID")
    """鸣潮记录ID"""
    auto_sign = fields.BooleanField(default=False, description="是否自动签到")
    """是否自动签到"""
    access_token = fields.CharField(255, null=True, description="access_token")
    """access_token"""
    device_id = fields.CharField(255, null=True, description="设备id")
    """设备id"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "waves_users"
        table_description = "鸣潮用户表"
