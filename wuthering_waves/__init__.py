from zhenxun.utils.manager.priority_manager import PriorityLifecycle

from .plugins import *  # noqa: F403
from .router import *  # noqa: F403
from .utils.manager.resource_manager import WsResourceManager


@PriorityLifecycle.on_startup(priority=5)
async def _():
    await WsResourceManager.download_emoji_resources()
