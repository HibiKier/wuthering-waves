import asyncio
from typing import Any, ClassVar, cast

from ....base_models import WwBaseResponse
from ....utils.utils import TimedCache
from ...const import ANN_CONTENT_URL, ANN_LIST_URL, GAME_ID
from ...headers import get_headers
from ..call import CallApi
from .models import AnnDetailResponse, AnnList, AnnPaginationData

cache = TimedCache(60 * 60 * 1)

detail_cache = TimedCache(60 * 60 * 24)


class AnnApi:
    event_type: ClassVar[dict[str, str]] = {"2": "资讯", "3": "公告", "1": "活动"}

    @classmethod
    async def get_ann_list_by_type(
        cls, event_type: str | None = None, page_size: int | None = None
    ) -> WwBaseResponse[AnnPaginationData]:
        """获取公告列表

        参数:
            event_type: 活动类型
            page_size: 每页数量

        返回:
            WwBaseResponse[AnnPaginationData]: 公告列表
        """
        data: dict[str, Any] = {"gameId": GAME_ID}
        if event_type:
            data["eventType"] = event_type
        if page_size:
            data["pageSize"] = page_size
        response = await CallApi.call_post(
            ANN_LIST_URL, header=await get_headers(), data=data
        )
        response.data = AnnPaginationData(**response.data)
        return response

    @classmethod
    async def get_ann(cls, page_size: int = 5) -> AnnList:
        """获取公告

        参数:
            page_size: 每页数量

        返回:
            List[AnnItem]: 公告列表
        """
        if cache.get("ann_list"):
            return cast(AnnList, cache.get("ann_list"))

        news_resp, announcement_resp, activity_resp = await asyncio.gather(
            *[
                cls.get_ann_list_by_type(event_type=event_type, page_size=page_size)
                for event_type in cls.event_type.keys()
            ]
        )

        combined_response = AnnList(
            news=news_resp.data.list,
            announcement=announcement_resp.data.list,
            activity=activity_resp.data.list,
        )
        cache.set("ann_list", combined_response)
        return combined_response

    @classmethod
    async def get_ann_detail(cls, query_id: str) -> AnnDetailResponse:
        """获取公告详情

        参数:
            query_id: 公告ID

        返回:
            AnnDetail: 公告详情
        """
        if detail_cache.get(query_id):
            return cast(AnnDetailResponse, detail_cache.get(query_id))
        data = {"isOnlyPublisher": 1, "postId": query_id, "showOrderType": 2}
        response = await CallApi.call_post(
            ANN_CONTENT_URL, header=await get_headers(), data=data
        )
        response.data = AnnDetailResponse(**response.data)
        detail_cache.set(query_id, response.data)
        return response.data
