from typing import Literal

from pydantic import BaseModel, Field

MAIN_URL = "https://top.camellya.xyz"
# MAIN_URL = "http://127.0.0.1:9001"

UPLOAD_URL = f"{MAIN_URL}/top/waves/upload"
GET_RANK_URL = f"{MAIN_URL}/top/waves/rank"
ONE_RANK_URL = f"{MAIN_URL}/top/waves/one"
UPLOAD_ABYSS_RECORD_URL = f"{MAIN_URL}/top/waves/abyss/upload"
GET_ABYSS_RECORD_URL = f"{MAIN_URL}/top/waves/abyss/record"
GET_HOLD_RATE_URL = f"{MAIN_URL}/api/waves/hold/rates"
GET_POOL_LIST = f"{MAIN_URL}/api/waves/pool/list"
GET_TOWER_APPEAR_RATE = f"{MAIN_URL}/api/waves/abyss/appear_rate"
UPLOAD_SLASH_RECORD_URL = f"{MAIN_URL}/top/waves/slash/upload"
GET_SLASH_APPEAR_RATE = f"{MAIN_URL}/api/waves/slash/appear_rate"

ABYSS_TYPE = Literal["l4", "m2", "r4", "a"]

ABYSS_TYPE_MAP = {
    "残响之塔": "l",
    "深境之塔": "m",
    "回音之塔": "r",
}

ABYSS_TYPE_MAP_REVERSE = {
    "l4": "残响之塔 - 4层",
    "m2": "深境之塔 - 2层",
    "r4": "回音之塔 - 4层",
}


class RankDetail(BaseModel):
    """排行榜详细信息模型

    用于存储角色排行榜的详细信息，包括玩家信息、角色信息和武器信息等
    """

    rank: int = Field(description="排名")
    user_id: str = Field(description="用户ID")
    username: str = Field(description="用户名称")
    alias_name: str = Field(description="别名", default="")
    kuro_name: str = Field(description="库洛账号名称", default="")
    waves_id: str = Field(description="波潮ID")
    char_id: int = Field(description="角色ID")
    level: int = Field(description="角色等级")
    chain: int = Field(description="角色命座数")
    weapon_id: int = Field(description="武器ID")
    weapon_level: int = Field(description="武器等级")
    weapon_reson_level: int = Field(description="武器共鸣等级")
    sonata_name: str = Field(description="奏章名称", default="")
    phantom_score: float = Field(description="幻影分数")
    phantom_score_bg: str = Field(description="幻影分数背景", default="")
    expected_damage: float = Field(description="预期伤害")
    expected_name: str = Field(description="预期伤害名称", default="")
