from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    MultiVar,
    Option,
    on_alconna,
)
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ...exceptions import APIResponseException, WavesException
from .data_source import DevelopDataSource

__plugin_meta__ = PluginMetadata(
    name="鸣潮角色养成",
    description="鸣潮角色养成",
    usage="""
    指令：
        ww角色养成
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1", menu_type="鸣潮").to_dict(),
)


_matcher = on_alconna(
    Alconna(
        "ww养成",
        Args["develop_list", MultiVar(str)],
        Option("-r", Args["role", str]),
    ),
    priority=5,
    block=True,
)

_matcher.shortcut(
    r"(?P<develop_list>([\u4e00-\u9fa5]+)(\s+[\u4e00-\u9fa5]+)*?)\s*(养成|培养|培养成本)",
    command="ww养成",
    arguments=["{develop_list}"],
    prefix=True,
)


@_matcher.handle()
async def _(
    session: Uninfo, arparma: Arparma, develop_list: tuple[str, ...], role: Match[str]
):
    try:
        role_id = role.result if role.available else None
        code_list = await DevelopDataSource.calc_develop_cost(
            session.user.id, role_id, develop_list
        )
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
