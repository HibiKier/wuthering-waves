from zhenxun.configs.path_config import DATA_PATH as ZX_DATA_PATH
from zhenxun.configs.path_config import IMAGE_PATH, TEMP_PATH
from zhenxun.utils.utils import ResourceDirManager

WW_TEMP_PATH = TEMP_PATH / "wuthering_waves"
WW_TEMP_PATH.mkdir(parents=True, exist_ok=True)

ResourceDirManager.add_temp_dir(WW_TEMP_PATH, True)

QR_TEMP_PATH = WW_TEMP_PATH / "qr"
QR_TEMP_PATH.mkdir(parents=True, exist_ok=True)

CAPTCHA_PATH = WW_TEMP_PATH / "captcha"
CAPTCHA_PATH.mkdir(parents=True, exist_ok=True)

DATA_PATH = ZX_DATA_PATH / "wuthering_waves"
DATA_PATH.mkdir(parents=True, exist_ok=True)


WW_IMAGE_PATH = IMAGE_PATH / "wuthering_waves"
WW_IMAGE_PATH.mkdir(parents=True, exist_ok=True)

EMOJI_PATH = WW_IMAGE_PATH / "emoji"
EMOJI_PATH.mkdir(parents=True, exist_ok=True)

ALIAS_PATH = DATA_PATH / "alias"
ALIAS_PATH.mkdir(parents=True, exist_ok=True)

CHAR_ALIAS_FILE = ALIAS_PATH / "char_alias.json"
"""角色别名文件"""
ECHO_ALIAS_FILE = ALIAS_PATH / "echo_alias.json"
"""声骸别名文件"""
SOUND_ALIAS_FILE = ALIAS_PATH / "sonata_alias.json"
"""声骸套装别名文件"""
WEAPON_ALIAS_FILE = ALIAS_PATH / "weapon_alias.json"
"""武器别名文件"""


MAP_PATH = DATA_PATH / "map"
MAP_PATH.mkdir(parents=True, exist_ok=True)

MAP_FILE = MAP_PATH / "map.json"
"""地图文件"""

ID2NAME_FILE = MAP_PATH / "id2name.json"
"""ID到名称的映射文件"""
