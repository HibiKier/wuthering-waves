from typing import ClassVar

import ujson as json

from zhenxun.services.log import logger
from zhenxun.utils.utils import cn2py

from ...config import LOG_COMMAND
from ...paths import (
    CHAR_ALIAS_FILE,
    ECHO_ALIAS_FILE,
    ID2NAME_FILE,
    SOUND_ALIAS_FILE,
    WEAPON_ALIAS_FILE,
)


class EntityManager:
    _char_alias: ClassVar[dict[str, list[str]]] = {}
    _echo_alias: ClassVar[dict[str, list[str]]] = {}
    _sound_alias: ClassVar[dict[str, list[str]]] = {}
    _weapon_alias: ClassVar[dict[str, list[str]]] = {}

    _id2name: ClassVar[dict[str, str]] = {}

    @classmethod
    def load_data(cls):
        with open(CHAR_ALIAS_FILE, encoding="utf-8") as f:
            cls._char_alias = json.load(f)
            logger.info(f"加载角色别名: {CHAR_ALIAS_FILE}", LOG_COMMAND)
        with open(ECHO_ALIAS_FILE, encoding="utf-8") as f:
            cls._echo_alias = json.load(f)
            logger.info(f"加载声骸别名: {ECHO_ALIAS_FILE}", LOG_COMMAND)
        with open(SOUND_ALIAS_FILE, encoding="utf-8") as f:
            cls._sound_alias = json.load(f)
            logger.info(f"加载声骸套装别名: {SOUND_ALIAS_FILE}", LOG_COMMAND)
        with open(WEAPON_ALIAS_FILE, encoding="utf-8") as f:
            cls._weapon_alias = json.load(f)
            logger.info(f"加载武器别名: {WEAPON_ALIAS_FILE}", LOG_COMMAND)
        with open(ID2NAME_FILE, encoding="utf-8") as f:
            cls._id2name = json.load(f)
            logger.info(f"加载ID到名称的映射: {ID2NAME_FILE}", LOG_COMMAND)

    @classmethod
    def get_weapon_alias(cls, weapon_name: str) -> str:
        """获取武器别名

        参数:
            weapon_name: 武器名

        返回:
            str: 武器别名
        """
        for i in cls._weapon_alias:
            if (weapon_name in i) or (weapon_name in cls._weapon_alias[i]):
                return i

        if "专武" in weapon_name:
            char_name = weapon_name.replace("专武", "")
            name = cls.get_char_alias(char_name)
            weapon_name = f"{name}专武"

        for i in cls._weapon_alias:
            if (weapon_name in i) or (weapon_name in cls._weapon_alias[i]):
                return i

        return weapon_name

    @classmethod
    def id_to_name(cls, id: int | str) -> str | None:
        """获取单位名称

        参数:
            id: 单位id

        返回:
            str | None: 单位名称
        """
        return cls._id2name.get(str(id))

    @classmethod
    def get_char_alias(cls, name: str) -> str | None:
        """获取角色别名

        参数:
            name: 角色名

        返回:
            str | None: 别名
        """
        for alias, aliases in cls._char_alias.items():
            if name in aliases:
                return alias
            if cn2py(name) == cn2py(alias):
                return alias
        return None

    @classmethod
    def get_echo_alias(cls, name: str) -> str | None:
        """获取声骸别名

        参数:
            name: 声骸名

        返回:
            str | None: 别名
        """
        for alias, aliases in cls._echo_alias.items():
            if name in aliases:
                return alias
            if cn2py(name) == cn2py(alias):
                return alias
        return None

    @classmethod
    def get_sound_alias(cls, name: str) -> str | None:
        """获取声骸别名

        参数:
            name: 声骸名

        返回:
            str | None: 别名
        """
        for alias, aliases in cls._sound_alias.items():
            if name in aliases:
                return alias
            if cn2py(name) == cn2py(alias):
                return alias
        return None

    @classmethod
    def name_to_id(cls, name: str) -> int | None:
        """获取角色ID

        参数:
            name: 角色名

        返回:
            int | None: 角色ID
        """
        if alias := cls.get_char_alias(name):
            return next(
                (int(id) for id, name in cls._id2name.items() if name == alias), None
            )
        else:
            return None


EntityManager.load_data()
