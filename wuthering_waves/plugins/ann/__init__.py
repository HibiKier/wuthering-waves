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
async def _(session: Uninfo, arparma: Arparma, ann_id: Match[str]):
    try:
        if ann_id.available:
            await AnnDataSource.get_ann_detail(ann_id.result)
        else:
            await AnnDataSource.get_ann()
        logger.info(
            "ww查询鸣潮公告成功，"
            f"公告ID：{ann_id.result if ann_id.available else '全部'}",
            arparma.header_result,
            session=session,
        )
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error("ww查询鸣潮公告失败", arparma.header_result, session=session, e=e)
        await MessageUtils.build_message("查询失败，请稍后再试").send()
