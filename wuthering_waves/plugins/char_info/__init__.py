from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, Subcommand, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .command import _matcher
from .data_source import CharInfoDataSource

__plugin_meta__ = PluginMetadata(
    name="鸣潮面板管理",
    description="鸣潮面板管理",
    usage="""
    刷新面板，如果多个角色可以通过 -r 指定角色ID，
    否则默认使用第一个角色

    指令：
        ww刷新面板 ?[角色] ?[-r [角色ID]]
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


@_matcher.assign("refresh")
async def _(
    bot: Bot, session: Uninfo, arparma: Arparma, char: Match[str], role: Match[str]
):
    char_name = [char.result] if char.available else "all"
    role_id = role.result if role.available else None
    try:
        await CharInfoDataSource.get_char_info(session.user.id, role_id, char_name)
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("ww刷新面板失败", arparma.header_result, session=session, e=e)
        await MessageUtils.build_message("查询失败，请稍后再试").send()
