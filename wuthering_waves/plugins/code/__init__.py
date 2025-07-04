from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import CodeDataSource

__plugin_meta__ = PluginMetadata(
    name="鸣潮兑换码",
    description="鸣潮兑换码查询",
    usage="""
    指令：
        ww兑换码
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna("ww兑换码"),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(session: Uninfo, arparma: Arparma):
    try:
        code_list = await CodeDataSource.get_code()
        if not code_list:
            await MessageUtils.build_message("目前暂无兑换码...").send()
            return
        await MessageUtils.build_message("\n".join(code_list)).send()
        logger.info(
            "ww查询鸣潮兑换码成功",
            arparma.header_result,
            session=session,
        )
    except APIResponseException as e:
        await MessageUtils.build_message(str(e)).send()
    except WavesException as e:
        await MessageUtils.build_message(str(e)).send()
    except Exception as e:
        logger.error(
            "ww查询鸣潮兑换码失败", arparma.header_result, session=session, e=e
        )
        await MessageUtils.build_message("查询失败，请稍后再试").send()
