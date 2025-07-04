from datetime import datetime
import time

import ujson as json

from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx

from .models import CodeModel

invalid_code_list = ("MINGCHAO",)


class CodeDataSource:
    url = "https://newsimg.5054399.com/comm/mlcxqcommon/static/wap/js/data_102.js?{}&callback=?&_={}"

    @classmethod
    async def get_code(cls) -> list[str] | None:
        text = ""
        try:
            now = datetime.now()
            time_string = (
                f"{now.year - 1900}{now.month - 1}{now.day}{now.hour}{now.minute}"
            )
            now_time = int(time.time() * 1000)
            url = cls.url.format(time_string, now_time)
            response = await AsyncHttpx.get(url)
            text = response.text.split("=", 1)[1].strip().rstrip(";")
            logger.debug(f"鸣潮兑换码列表: {text}")
            json_data = json.loads(text)
            return cls.__format([CodeModel(**item) for item in json_data])
        except Exception as e:
            logger.error(f"鸣潮兑换码列表获取失败 text: {text}", e=e)
            return None

    @classmethod
    def __format(cls, code_list: list[CodeModel]) -> list[str]:
        msgs = []
        for code in code_list:
            if code.is_fail == "1":
                continue
            if code.order in invalid_code_list or not code.order:
                continue
            msg = [f"兑换码: {code.order}", f"奖励: {code.reward}", code.label, "\n"]
            msgs.append("\n".join(msg))
        return msgs
