from typing import Literal

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.builtin_plugins.wuthering_waves.waves_api.api import ann
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import WikiDataSource

__plugin_meta__ = PluginMetadata(
    name="鸣潮个人日历",
    description="鸣潮个人日历查询",
    usage="""
    指令：
        ww日历
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww日历"),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(bot: Bot, session: Uninfo, arparma: Arparma, ann_id: Match[str]):
    try:
        await WikiDataSource.get_wiki_home()
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("查询公告失败", session=session, e=e)
        await MessageUtils.build_message("查询失败，请稍后再试").send()
