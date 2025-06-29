from pydantic import BaseModel, Field

from zhenxun.configs.config import Config as ZxConfig

GAME_NAME = "[鸣潮]"

LOG_COMMAND = "WutheringWaves"

WEB_PREFIX = "/zhenxun/waves"


class LoginConfig(BaseModel):
    qr_login: bool = Field(default=False, description="是否启用二维码登录")
    captcha_provider: str | None = Field(default=None, description="验证码提供者")
    captcha_appkey: str | None = Field(default=None, description="验证码APPKEY")


class Config(BaseModel):
    login: LoginConfig = Field(default_factory=LoginConfig)
    is_test: bool = Field(default=True, description="是否为测试环境")


ZxConfig.add_plugin_config(
    "wuthering_waves", "config", Config(), help="鸣潮基础配置项", type=Config
)


config: Config = ZxConfig.get_config("wuthering_waves", "config")
