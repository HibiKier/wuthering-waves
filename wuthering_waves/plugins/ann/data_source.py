from typing import cast

from ...exceptions import WavesException
from ...utils.utils import TimedCache
from ...waves_api.api.ann import AnnApi

cache = TimedCache(60 * 60 * 12)


class AnnDataSource:
    @classmethod
    async def get_ann(cls, page_size: int = 5):
        ann_list = await AnnApi.get_ann(page_size)
        for ann_type in ["activity", "announcement", "news"]:
            for ann in getattr(ann_list, ann_type, []):
                cache.set(ann.id, ann.post_id)
        print(ann_list)

    @classmethod
    async def get_ann_detail(cls, query_id: str):
        query_id = cast(str, cache.get(query_id))
        if not query_id:
            raise WavesException("公告ID不存在，请重新获取公共信息查看")
        ann_detail = await AnnApi.get_ann_detail(query_id)
        print(ann_detail)
