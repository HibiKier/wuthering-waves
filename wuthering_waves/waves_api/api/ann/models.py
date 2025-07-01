import builtins
from datetime import datetime

from pydantic import BaseModel, Field


class AnnItem(BaseModel):
    cover_url: str = Field(..., alias="coverUrl", description="封面图URL")
    """封面图URL"""
    event_type: int = Field(..., alias="eventType", description="活动类型")
    """活动类型"""
    first_publish_time: int = Field(
        ..., alias="firstPublishTime", description="首次发布时间戳(ms)"
    )
    """首次发布时间戳(ms)"""
    game_id: int = Field(..., alias="gameId", description="游戏ID")
    """游戏ID"""
    id: str = Field(..., description="活动ID")
    """活动ID"""
    post_id: str = Field(..., alias="postId", description="帖子ID")
    """帖子ID"""
    post_title: str = Field(..., alias="postTitle", description="帖子标题")
    """帖子标题"""
    publish_time: int = Field(..., alias="publishTime", description="发布时间戳(ms)")
    """发布时间戳(ms)"""
    shelve_time: int = Field(..., alias="shelveTime", description="上架时间戳(ms)")
    """上架时间戳(ms)"""
    show_type: int | None = Field(None, alias="showType", description="展示类型")
    """展示类型"""

    # 添加时间戳转换方法
    @property
    def publish_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.publish_time / 1000)


class AnnPaginationData(BaseModel):
    end_row: str = Field(..., alias="endRow", description="结束行号")
    """结束行号"""
    has_next_page: bool = Field(..., alias="hasNextPage", description="是否有下一页")
    """是否有下一页"""
    has_previous_page: bool = Field(
        ..., alias="hasPreviousPage", description="是否有上一页"
    )
    """是否有上一页"""
    is_first_page: bool = Field(..., alias="isFirstPage", description="是否第一页")
    """是否第一页"""
    is_last_page: bool = Field(..., alias="isLastPage", description="是否最后一页")
    """是否最后一页"""
    list: builtins.list[AnnItem] = Field(..., description="帖子列表数据")
    """帖子列表数据"""
    navigate_first_page: int = Field(
        ..., alias="navigateFirstPage", description="导航第一页"
    )
    """导航第一页"""
    navigate_last_page: int = Field(
        ..., alias="navigateLastPage", description="导航最后一页"
    )
    """导航最后一页"""
    navigate_pages: int = Field(..., alias="navigatePages", description="导航页数")
    """导航页数"""
    navigate_page_nums: builtins.list[int] = Field(
        ..., alias="navigatepageNums", description="导航页码列表"
    )
    """导航页码列表"""
    next_page: int = Field(..., alias="nextPage", description="下一页页码")
    """下一页页码"""
    page_num: int = Field(..., alias="pageNum", description="当前页码")
    """当前页码"""
    page_size: int = Field(..., alias="pageSize", description="每页数量")
    """每页数量"""
    pages: int = Field(..., description="总页数")
    """总页数"""
    pre_page: int = Field(..., alias="prePage", description="上一页页码")
    """上一页页码"""
    size: int = Field(..., description="当前页实际数量")
    """当前页实际数量"""
    start_row: str = Field(..., alias="startRow", description="起始行号")
    """起始行号"""
    total: str = Field(..., description="总记录数")
    """总记录数"""


class AnnList(BaseModel):
    news: list[AnnItem] = Field(..., description="新闻列表")
    """新闻列表"""
    announcement: list[AnnItem] = Field(..., description="公告列表")
    """公告列表"""
    activity: list[AnnItem] = Field(..., description="活动列表")
    """活动列表"""


class CoverImage(BaseModel):
    img_height: int = Field(..., alias="imgHeight", description="图片高度")
    """图片高度"""
    img_width: int = Field(..., alias="imgWidth", description="图片宽度")
    """图片宽度"""
    index: int = Field(..., description="图片索引")
    """图片索引"""
    point_offset_x: int = Field(..., alias="pointOffsetX", description="X轴偏移")
    """X轴偏移"""
    point_offset_y: int = Field(..., alias="pointOffsetY", description="Y轴偏移")
    """Y轴偏移"""
    url: str = Field(..., description="图片URL")
    """图片URL"""


class ContentItem(BaseModel):
    content: str | None = Field(None, description="内容文本")
    """内容文本"""
    content_type: int = Field(..., alias="contentType", description="内容类型")
    """内容类型"""
    img_height: int = Field(..., alias="imgHeight", description="图片高度(图片内容时)")
    """图片高度(图片内容时)"""
    img_width: int = Field(..., alias="imgWidth", description="图片宽度(图片内容时)")
    """图片宽度(图片内容时)"""


class GameForum(BaseModel):
    filter_offical_user_ids: str = Field(
        ..., alias="filterOfficalUserIds", description="过滤官方用户ID"
    )
    """过滤官方用户ID"""
    forum_data_type: int = Field(..., alias="forumDataType", description="论坛数据类型")
    """论坛数据类型"""
    forum_list_show_type: int = Field(
        ..., alias="forumListShowType", description="论坛列表展示类型"
    )
    """论坛列表展示类型"""
    forum_type: int = Field(..., alias="forumType", description="论坛类型")
    """论坛类型"""
    forum_ui_type: int = Field(..., alias="forumUiType", description="论坛UI类型")
    """论坛UI类型"""
    id: int = Field(..., description="论坛ID")
    """论坛ID"""
    is_official: int = Field(..., alias="isOfficial", description="是否官方")
    """是否官方"""
    is_special: int = Field(..., alias="isSpecial", description="是否特殊")
    """是否特殊"""
    name: str = Field(..., description="论坛名称")
    """论坛名称"""
    range_day: int = Field(..., alias="rangeDay", description="范围天数")
    """范围天数"""
    sort: int = Field(..., description="排序")
    """排序"""


class Topic(BaseModel):
    post_id: str = Field(..., alias="postId", description="帖子ID")
    """帖子ID"""
    topic_id: int = Field(..., alias="topicId", description="话题ID")
    """话题ID"""
    topic_name: str = Field(..., alias="topicName", description="话题名称")
    """话题名称"""


class AnnDetail(BaseModel):
    appealing: bool = Field(..., description="是否申诉中")
    """是否申诉中"""
    best_definition: str | None = Field(
        None, alias="bestDefinition", description="最佳清晰度"
    )
    """最佳清晰度"""
    browse_count: str = Field(..., alias="browseCount", description="浏览数")
    """浏览数"""
    can_play: bool | None = Field(None, alias="canPlay", description="是否可以播放")
    """是否可以播放"""
    collection_count: int = Field(..., alias="collectionCount", description="收藏数")
    """收藏数"""
    comment_count: int = Field(..., alias="commentCount", description="评论数")
    """评论数"""
    company_event_type: int = Field(
        ..., alias="companyEventType", description="公司活动类型"
    )
    """公司活动类型"""
    cover_images: list[CoverImage] = Field(
        ..., alias="coverImages", description="封面图片列表"
    )
    """封面图片列表"""
    create_timestamp: str = Field(
        ..., alias="createTimestamp", description="创建时间戳"
    )
    """创建时间戳"""
    game_forum_id: int = Field(..., alias="gameForumId", description="游戏论坛ID")
    """游戏论坛ID"""
    game_forum_vo: GameForum = Field(
        ..., alias="gameForumVo", description="游戏论坛信息"
    )
    """游戏论坛信息"""
    game_id: int = Field(..., alias="gameId", description="游戏ID")
    """游戏ID"""
    game_name: str = Field(..., alias="gameName", description="游戏名称")
    """游戏名称"""
    head_code_url: str = Field(..., alias="headCodeUrl", description="头像URL")
    """头像URL"""
    id: str = Field(..., description="帖子ID")
    """帖子ID"""
    identify_classify: int = Field(
        ..., alias="identifyClassify", description="身份分类"
    )
    """身份分类"""
    identify_names: str = Field(..., alias="identifyNames", description="身份名称")
    """身份名称"""
    ip_region: str = Field(..., alias="ipRegion", description="IP地区")
    """IP地区"""
    is_copyright: bool = Field(..., alias="isCopyright", description="是否版权内容")
    """是否版权内容"""
    is_elite: int = Field(..., alias="isElite", description="是否精华")
    """是否精华"""
    is_lock: int = Field(..., alias="isLock", description="是否锁定")
    """是否锁定"""
    is_mine: int = Field(..., alias="isMine", description="是否我的")
    """是否我的"""
    is_official: int = Field(..., alias="isOfficial", description="是否官方")
    """是否官方"""
    is_recommend: int = Field(..., alias="isRecommend", description="是否推荐")
    """是否推荐"""
    is_top: int = Field(..., alias="isTop", description="是否置顶")
    """是否置顶"""
    is_trans_code: bool = Field(..., alias="isTransCode", description="是否转码")
    """是否转码"""
    last_edit_ip_region: str = Field(
        ..., alias="lastEditIpRegion", description="最后编辑IP地区"
    )
    """最后编辑IP地区"""
    like_count: int = Field(..., alias="likeCount", description="点赞数")
    """点赞数"""
    play_count: int = Field(..., alias="playCount", description="播放数")
    """播放数"""
    post_content: list[ContentItem] = Field(
        ..., alias="postContent", description="帖子内容"
    )
    """帖子内容"""
    post_h5_content: str = Field(..., alias="postH5Content", description="H5格式内容")
    """H5格式内容"""
    post_new_h5_content: str = Field(
        ..., alias="postNewH5Content", description="新版H5格式内容"
    )
    """新版H5格式内容"""
    post_time: str = Field(..., alias="postTime", description="发布时间")
    """发布时间"""
    post_title: str = Field(..., alias="postTitle", description="帖子标题")
    """帖子标题"""
    post_type: int = Field(..., alias="postType", description="帖子类型")
    """帖子类型"""
    post_user_id: str = Field(..., alias="postUserId", description="发帖用户ID")
    """发帖用户ID"""
    publish_type: int = Field(..., alias="publishType", description="发布类型")
    """发布类型"""
    reason: str | None = Field(None, description="原因")
    """原因"""
    review_status: int = Field(..., alias="reviewStatus", description="审核状态")
    """审核状态"""
    show_range: int = Field(..., alias="showRange", description="显示范围")
    """显示范围"""
    topic_list: list[Topic] = Field(..., alias="topicList", description="话题列表")
    """话题列表"""
    user_head_code: str = Field(..., alias="userHeadCode", description="用户头像代码")
    """用户头像代码"""
    user_level: int = Field(..., alias="userLevel", description="用户等级")
    """用户等级"""
    user_name: str = Field(..., alias="userName", description="用户名")
    """用户名"""
    video_height: str | None = Field(None, alias="videoHeight", description="视频高度")
    """视频高度"""
    video_id: str | None = Field(None, alias="videoId", description="视频ID")
    """视频ID"""
    video_width: str | None = Field(None, alias="videoWidth", description="视频宽度")
    """视频宽度"""


class AnnDetailResponse(BaseModel):
    activity_id: str = Field(..., alias="activityId", description="活动ID")
    """活动ID"""
    game_id: int = Field(..., alias="gameId", description="游戏ID")
    """游戏ID"""
    is_collect: int = Field(..., alias="isCollect", description="是否收藏")
    """是否收藏"""
    is_follow: int = Field(..., alias="isFollow", description="是否关注")
    """是否关注"""
    is_like: int = Field(..., alias="isLike", description="是否点赞")
    """是否点赞"""
    post_detail: AnnDetail = Field(..., alias="postDetail", description="帖子详情")
    """帖子详情"""
