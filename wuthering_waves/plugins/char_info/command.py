from nonebot_plugin_alconna import Alconna, Args, Option, Subcommand, on_alconna

_matcher = on_alconna(
    Alconna(
        "ww-board",
        Option("-r", Args["role", str]),
        Subcommand("refresh", Args["char?", str]),
    ),
    priority=5,
    block=True,
)

_matcher.shortcut(
    r"ww刷新面板\s*(?P<name>.*)",
    command="ww-board",
    arguments=["refresh", "{name}"],
    prefix=True,
)
