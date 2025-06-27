from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.utils.utils import ResourceDirManager

WW_TEMP_PATH = TEMP_PATH / "wuthering_waves"
WW_TEMP_PATH.mkdir(parents=True, exist_ok=True)

ResourceDirManager.add_temp_dir(WW_TEMP_PATH, True)

QR_TEMP_PATH = WW_TEMP_PATH / "qr"
QR_TEMP_PATH.mkdir(parents=True, exist_ok=True)

CAPTCHA_PATH = WW_TEMP_PATH / "captcha"
CAPTCHA_PATH.mkdir(parents=True, exist_ok=True)
