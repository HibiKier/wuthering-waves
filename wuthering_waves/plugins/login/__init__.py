from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, MultiVar, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...config import LOG_COMMAND
from ...exceptions import APIResponseException, WavesException
from .data_source import LoginManager

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
    Alconna("ww登录", Args["login_info?", MultiVar(str)]), priority=5, block=True
)


@_matcher.handle()
async def _(
    bot: Bot, session: Uninfo, arparma: Arparma, login_info: Match[tuple[str, ...]]
):
    try:
        if login_info.available:
            login_text = login_info.result
            if len(login_text) < 2:
                await _matcher.send("请输入正确的登录信息: 手机号 验证码")
            result = await LoginManager.code_login(
                session.user.id,
                f"{login_info.result[0]} {login_info.result[1]}",
            )
        else:
            result = await LoginManager.page_login(
                bot, session.user.id, session.group.id if session.group else None
            )
        await MessageUtils.build_message(result).send(reply_to=True)
    except APIResponseException as e:
        logger.error("ww登录失败", LOG_COMMAND, session=session, e=e)
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        logger.error("ww登录失败", LOG_COMMAND, session=session, e=e)
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("ww登录失败", LOG_COMMAND, session=session, e=e)
        await MessageUtils.build_message("登录未知错误，请稍后再试").send()
