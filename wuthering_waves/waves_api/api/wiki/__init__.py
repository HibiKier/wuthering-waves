from ...const import WIKI_HOME_URL
from ...headers import get_headers
from ..call import CallApi
from .models import WikiHome


class WikiApi:
    @classmethod
    async def get_wiki_home(cls):
        """获取wiki数据"""
        headers = await get_headers()
        headers["wiki_type"] = "9"
        response = await CallApi.call_post(WIKI_HOME_URL, header=headers)
        return WikiHome(**response.data)
