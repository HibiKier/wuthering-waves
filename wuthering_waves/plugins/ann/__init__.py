from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import AnnDataSource

__plugin_meta__ = PluginMetadata(
    name="鸣潮公告",
    description="鸣潮公共信息查询",
    usage="""
    指令：
        ww公告
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww公告", Args["ann_id?", str]),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(bot: Bot, session: Uninfo, arparma: Arparma, ann_id: Match[str]):
    try:
        if ann_id.available:
            await AnnDataSource.get_ann_detail(ann_id.result)
        else:
            await AnnDataSource.get_ann()
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("查询公告失败", session=session, e=e)
        await MessageUtils.build_message("查询失败，请稍后再试").send()
