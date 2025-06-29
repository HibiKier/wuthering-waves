from datetime import datetime

from pydantic import BaseModel, Field


class EmojiItem(BaseModel):
    img_url: str = Field(..., alias="imgUrl", description="表情图片的URL地址")
    img_size: str = Field(
        ..., alias="imgSize", description="表情图片的文件大小（字节）"
    )
    name: str = Field(..., description="表情名称")
    package_id: str = Field(..., alias="packageId", description="所属表情包的ID")
    index: int = Field(..., description="在当前包中的排序索引", ge=1)
    id: str = Field(..., description="表情的唯一标识ID")


class EmojiPackage(BaseModel):
    creat_time: datetime = Field(..., alias="creatTime", description="表情包创建时间")
    emoji_list: list[EmojiItem] = Field(
        ..., alias="emojiList", description="包含的表情列表", min_items=1
    )
    active_time: datetime = Field(..., alias="activeTime", description="表情包生效时间")
    main_img_url: str = Field(..., alias="mainImgUrl", description="表情包封面图URL")
    state_code: int = Field(
        ...,
        alias="stateCode",
        description="状态编码（1=未生效，2=生效中，3=已下架）",
    )
    timing_active: int = Field(
        ..., alias="timingActive", description="是否定时生效（0=否，1=是）", ge=0, le=1
    )
    update_time: datetime = Field(..., alias="updateTime", description="最后更新时间")
    id: str = Field(..., description="表情包唯一ID")
    package_size: str = Field(
        ..., alias="packageSize", description="表情包总大小（带单位）"
    )
    state: str = Field(..., description="状态描述")
    title: str = Field(..., description="表情包标题", max_length=50)
