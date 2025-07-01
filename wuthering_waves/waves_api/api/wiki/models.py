import builtins
from typing import Any

from pydantic import BaseModel, Field


class LinkConfig(BaseModel):
    link_url: str | None = Field(None, alias="linkUrl", description="链接URL")
    """链接URL"""
    link_type: int = Field(..., alias="linkType", description="链接类型")
    """链接类型"""
    catalogue_id: int | None = Field(None, alias="catalogueId", description="目录ID")
    """目录ID"""
    entry_id: str | None = Field(None, alias="entryId", description="条目ID")
    """条目ID"""


class FeedbackItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    content_url: str = Field(..., alias="contentUrl", description="内容URL")
    """内容URL"""
    content_url_real_name: str = Field(
        ..., alias="contentUrlRealName", description="内容URL真实名称"
    )
    """内容URL真实名称"""
    disable_link_config: bool | None = Field(
        None, alias="disableLinkConfig", description="禁用链接配置"
    )
    """禁用链接配置"""
    fixed: bool | None = Field(None, alias="fixed", description="是否固定")
    """是否固定"""
    type: str | None = Field(None, alias="type", description="类型")
    """类型"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""


class Background(BaseModel):
    x: str = Field(..., alias="x", description="X坐标")
    """X坐标"""
    y: str = Field(..., alias="y", description="Y坐标")
    """Y坐标"""
    url: str = Field(..., alias="url", description="背景图片URL")
    """背景图片URL"""


class MoreInfo(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    visible: bool = Field(..., alias="visible", description="是否可见")
    """是否可见"""
    title: str | None = Field(None, alias="title", description="标题")
    """标题"""


class ContentChild(BaseModel):
    children: list[Any] = Field(..., alias="children", description="子节点")
    """子节点"""  # 根据数据，这里是空列表
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    checked: bool = Field(..., alias="checked", description="是否选中")
    """是否选中"""
    id: int = Field(..., alias="id", description="ID")
    """ID"""
    sort: int = Field(..., alias="sort", description="排序")
    """排序"""
    is_fixed: int = Field(..., alias="isFixed", description="是否固定")
    """是否固定"""
    key: int = Field(..., alias="key", description="键")
    """键"""
    parent_id: int = Field(..., alias="parentId", description="父ID")
    """父ID"""


class CatalogueContent(BaseModel):
    children: list[ContentChild] = Field(..., alias="children", description="子目录")
    """子目录"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    id: int = Field(..., alias="id", description="ID")
    """ID"""
    sort: int = Field(..., alias="sort", description="排序")
    """排序"""
    is_fixed: int = Field(..., alias="isFixed", description="是否固定")
    """是否固定"""
    key: int = Field(..., alias="key", description="键")
    """键"""
    parent_id: int = Field(..., alias="parentId", description="父ID")
    """父ID"""


class MultiListItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    content_url: str = Field(..., alias="contentUrl", description="内容URL")
    """内容URL"""
    content_url_real_name: str = Field(
        ..., alias="contentUrlRealName", description="内容URL真实名称"
    )
    """内容URL真实名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    id: str = Field(..., alias="id", description="ID")
    """ID"""
    list: builtins.list[dict[str, Any]] = Field(..., alias="list", description="列表")
    """列表"""  # 包含链接配置和名称的字典列表
    title: str = Field(..., alias="title", description="标题")
    """标题"""


class MainModule(BaseModel):
    toolslayer_visible: bool = Field(
        ..., alias="toolslayerVisible", description="工具层是否可见"
    )
    """工具层是否可见"""
    more: MoreInfo = Field(..., alias="more", description="更多信息")
    """更多信息"""
    edit_layer_hide: bool = Field(
        ..., alias="editLayerHide", description="编辑层是否隐藏"
    )
    """编辑层是否隐藏"""
    aside_line_visible: bool = Field(
        ..., alias="asideLineVisible", description="侧边线是否可见"
    )
    """侧边线是否可见"""
    id: str = Field(..., alias="id", description="ID")
    """ID"""
    icon_url: str | None = Field(None, alias="iconUrl", description="图标URL")
    """图标URL"""
    type: str | None = Field(None, alias="type", description="类型")
    """类型"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    content: Any = Field(..., alias="content", description="模块内容")
    """模块内容"""  # 根据type可以是CatalogueContent或List[MultiListItem]


class ShortcutItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    content_url: str = Field(..., alias="contentUrl", description="内容URL")
    """内容URL"""
    is_newest: bool = Field(..., alias="isNewest", description="是否最新")
    """是否最新"""
    id: str = Field(..., alias="id", description="ID")
    """ID"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    image_name_map: dict[str, str] = Field(
        ..., alias="imageNameMap", description="图片名称映射"
    )
    """图片名称映射"""
    mobile_img_url: str = Field(..., alias="mobileImgUrl", description="移动端图片URL")
    """移动端图片URL"""


class Shortcuts(BaseModel):
    toolslayer_visible: bool = Field(
        ..., alias="toolslayerVisible", description="工具层是否可见"
    )
    """工具层是否可见"""
    more: MoreInfo = Field(..., alias="more", description="更多信息")
    """更多信息"""
    edit_layer_hide: bool = Field(
        ..., alias="editLayerHide", description="编辑层是否隐藏"
    )
    """编辑层是否隐藏"""
    aside_line_visible: bool = Field(
        ..., alias="asideLineVisible", description="侧边线是否可见"
    )
    """侧边线是否可见"""
    id: str = Field(..., alias="id", description="ID")
    """ID"""
    icon_url: str = Field(..., alias="iconUrl", description="图标URL")
    """图标URL"""
    type: str = Field(..., alias="type", description="类型")
    """类型"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    content: list[ShortcutItem] = Field(
        ..., alias="content", description="快捷方式内容"
    )
    """快捷方式内容"""


class BannerItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    date_range: list[str] = Field(..., alias="dateRange", description="日期范围")
    """日期范围"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    describe: str = Field(..., alias="describe", description="描述")
    """描述"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    url: str = Field(..., alias="url", description="URL")
    """URL"""


class CountDownRepeat(BaseModel):
    end_date: str = Field(..., alias="endDate", description="结束日期")
    """结束日期"""
    is_never_end: bool = Field(..., alias="isNeverEnd", description="是否永不结束")
    """是否永不结束"""
    repeat_interval: int = Field(..., alias="repeatInterval", description="重复间隔")
    """重复间隔"""
    data_ranges: list[dict[str, Any]] = Field(
        ..., alias="dataRanges", description="数据范围"
    )
    """数据范围"""  # 字典列表


class CountDown(BaseModel):
    date_range: list[str] = Field(..., alias="dateRange", description="日期范围")
    """日期范围"""
    repeat: CountDownRepeat = Field(..., alias="repeat", description="重复配置")
    """重复配置"""
    precision: str = Field(..., alias="precision", description="精度")
    """精度"""
    type: str = Field(..., alias="type", description="类型")
    """类型"""


class ImageItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    img: str = Field(..., alias="img", description="图片URL")
    """图片URL"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""


class InnerTab(BaseModel):
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    description: str = Field(..., alias="description", description="描述")
    """描述"""


class Tab(BaseModel):
    imgs: list[ImageItem] = Field(..., alias="imgs", description="图片列表")
    """图片列表"""
    inner_tabs: list[InnerTab] = Field(..., alias="innerTabs", description="内部标签页")
    """内部标签页"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    img_mode: str = Field(..., alias="imgMode", description="图片模式")
    """图片模式"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    description: str = Field(..., alias="description", description="描述")
    """描述"""
    count_down: CountDown = Field(..., alias="countDown", description="倒计时")
    """倒计时"""


class EventsSideContent(BaseModel):
    visible: bool = Field(..., alias="visible", description="是否可见")
    """是否可见"""
    tabs: list[Tab] = Field(..., alias="tabs", description="标签页列表")
    """标签页列表"""


class HotContentSideItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    content_url: str = Field(..., alias="contentUrl", description="内容URL")
    """内容URL"""
    content_url_real_name: str = Field(
        ..., alias="contentUrlRealName", description="内容URL真实名称"
    )
    """内容URL真实名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    count_down: CountDown | None = Field(None, alias="countDown", description="倒计时")
    """倒计时"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""


class QuickEntryItem(BaseModel):
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    content_url: str = Field(..., alias="contentUrl", description="内容URL")
    """内容URL"""
    content_url_real_name: str = Field(
        ..., alias="contentUrlRealName", description="内容URL真实名称"
    )
    """内容URL真实名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""


class GuideQRCodeContent(BaseModel):
    ico_url: str = Field(..., alias="icoUrl", description="图标URL")
    """图标URL"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    title_url_config: LinkConfig = Field(
        ..., alias="titleUrlConfig", description="标题URL配置"
    )
    """标题URL配置"""
    content: str = Field(..., alias="content", description="内容")
    """内容"""


class SideModule(BaseModel):
    toolslayer_visible: bool = Field(
        ..., alias="toolslayerVisible", description="工具层是否可见"
    )
    """工具层是否可见"""
    more: MoreInfo = Field(..., alias="more", description="更多信息")
    """更多信息"""
    unique: bool = Field(..., alias="unique", description="是否唯一")
    """是否唯一"""
    edit_layer_hide: bool = Field(
        ..., alias="editLayerHide", description="编辑层是否隐藏"
    )
    """编辑层是否隐藏"""
    aside_line_visible: bool = Field(
        ..., alias="asideLineVisible", description="侧边线是否可见"
    )
    """侧边线是否可见"""
    id: str = Field(..., alias="id", description="ID")
    """ID"""
    icon_url: str | None = Field(None, alias="iconUrl", description="图标URL")
    """图标URL"""
    type: str | None = Field(None, alias="type", description="类型")
    """类型"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    content: Any = Field(..., alias="content", description="模块内容")
    """模块内容"""  # 根据type可以是EventsSideContent, List[HotContentSideItem], List[QuickEntryItem], List[GuideQRCodeContent]或空列表


class AnnouncementLinkCard(BaseModel):
    img_url: str = Field(..., alias="imgUrl", description="图片URL")
    """图片URL"""
    link_config: LinkConfig = Field(..., alias="linkConfig", description="链接配置")
    """链接配置"""
    title: str = Field(..., alias="title", description="标题")
    """标题"""
    content: str = Field(..., alias="content", description="内容")
    """内容"""


class AnnouncementItem(BaseModel):
    link_card_visible: bool = Field(
        ..., alias="linkCardVisible", description="链接卡片是否可见"
    )
    """链接卡片是否可见"""
    name: str = Field(..., alias="name", description="名称")
    """名称"""
    active: bool = Field(..., alias="active", description="是否激活")
    """是否激活"""
    link_card: AnnouncementLinkCard = Field(
        ..., alias="linkCard", description="链接卡片"
    )
    """链接卡片"""
    content: str = Field(..., alias="content", description="内容")
    """内容"""


class ContentJson(BaseModel):
    feedback: list[FeedbackItem] = Field(..., alias="feedback", description="反馈列表")
    """反馈列表"""
    background: Background = Field(..., alias="background", description="背景配置")
    """背景配置"""
    main_modules: list[MainModule] = Field(
        ..., alias="mainModules", description="主模块列表"
    )
    """主模块列表"""
    shortcuts: Shortcuts = Field(..., alias="shortcuts", description="快捷导航")
    """快捷导航"""
    banner: list[BannerItem] = Field(..., alias="banner", description="横幅列表")
    """横幅列表"""
    side_modules: list[SideModule] = Field(
        ..., alias="sideModules", description="侧边模块列表"
    )
    """侧边模块列表"""
    announcement: list[AnnouncementItem] | None = Field(
        None, alias="announcement", description="公告列表"
    )
    """公告列表"""


class WikiHome(BaseModel):
    id: int = Field(..., alias="id", description="ID")
    """ID"""
    sort: Any | None = Field(None, alias="sort", description="排序")
    """排序"""
    status: int = Field(..., alias="status", description="状态")
    """状态"""
    check_status: int = Field(..., alias="checkStatus", description="检查状态")
    """检查状态"""
    version: Any | None = Field(None, alias="version", description="版本")
    """版本"""
    online_version: Any | None = Field(
        None, alias="onlineVersion", description="在线版本"
    )
    """在线版本"""
    content_json: ContentJson = Field(..., alias="contentJson", description="内容JSON")
    """内容JSON"""
