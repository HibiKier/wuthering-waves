from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, MultiVar, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.builtin_plugins.wuthering_waves.plugins.ww_login.data_source import (
    LoginManager,
)
from zhenxun.configs.utils import PluginExtraData
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="ww登录",
    description="鸣潮登录",
    usage="""
    指令：
        ww登录
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww登录", Args["login_info?", MultiVar[str]]), priority=5, block=True
)


@_matcher.handle()
async def _(
    bot: Bot, session: Uninfo, arparma: Arparma, login_info: Match[tuple[str, ...]]
):
    if login_info.available:
        login_text = login_info.result
        if len(login_text) < 2:
            await _matcher.send("请输入正确的登录信息: 手机号 验证码")
        result = await LoginManager.code_login(
            bot,
            session.user.id,
            session.group.id if session.group else None,
            f"{login_info.result[0]} {login_info.result[1]}",
        )
    else:
        result = await LoginManager.page_login(
            bot, session.user.id, session.group.id if session.group else None
        )
    await MessageUtils.build_message(result).send(reply_to=True)
