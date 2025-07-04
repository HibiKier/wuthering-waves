from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import CharListDataSource

__plugin_meta__ = PluginMetadata(
    name="练度统计",
    description="鸣潮练度统计",
    usage="""
    指令：
        ww练度统计
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww练度统计", Args["role?", str]),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: Uninfo, arparma: Arparma, role: Match[str]):
    role_id = role.result if role.available else None
    try:
        await CharListDataSource.get_char_list(session.user.id, role_id)
        logger.info(
            f"ww查询练度统计成功: {role_id}",
            arparma.header_result,
            session=session,
        )
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    # except Exception as e:
    #     logger.error("ww查询练度统计失败", arparma.header_result, session=session, e=e)
    #     await MessageUtils.build_message("查询失败，请稍后再试").send()
