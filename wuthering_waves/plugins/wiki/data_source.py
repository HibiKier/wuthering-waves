from ...waves_api.api.wiki import WikiApi


class WikiDataSource:
    @classmethod
    async def get_wiki_home(cls):
        """获取wiki首页数据"""
        wiki_home = await WikiApi.get_wiki_home()
        print(wiki_home)
