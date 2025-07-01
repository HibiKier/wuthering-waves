from typing import Literal

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import AbyssDataSource

__plugin_meta__ = PluginMetadata(
    name="ww深渊",
    description="鸣潮深渊查询",
    usage="""
    指令：
        ww查询深渊 超载/稳定/实验
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww查询深渊", Args["area?", Literal["超载", "稳定", "实验"]]),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(bot: Bot, session: Uninfo, arparma: Arparma, area: Match[str]):
    try:
        area_str = area.result if area.available else ""
        await AbyssDataSource.get_abyss(area_str, session.user.id, None)
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("查询深渊失败", session=session, e=e)
        await MessageUtils.build_message("查询失败，请稍后再试").send()
