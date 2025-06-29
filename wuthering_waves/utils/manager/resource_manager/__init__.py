import os
from pathlib import Path

import aiofiles

from zhenxun.builtin_plugins.wuthering_waves.paths import EMOJI_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx

from ....base_models import WwBaseResponse
from ....config import LOG_COMMAND
from ....models.emoji import EmojiItem, EmojiPackage
from .models import EmojiPackage as EmojiPackageModel


class WsResourceManager:
    EMOJI_URL = "https://api.kurobbs.com/user/emoji/queryAll"

    @classmethod
    async def download_emoji_resources(cls):
        logger.info("开始下载获取鸣潮表情资源...", LOG_COMMAND)
        await cls.call_emoji_resources()
        logger.info("开始下载鸣潮表情资源...", LOG_COMMAND)
        await cls.download_emojis()
        logger.info("鸣潮表情资源下载完成", LOG_COMMAND)

    @classmethod
    async def call_emoji_resources(cls):
        """下载表情资源并存储到数据库"""
        response = await AsyncHttpx.post(cls.EMOJI_URL)
        response.raise_for_status()

        ww_response = WwBaseResponse(**response.json())
        emoji_packages = [EmojiPackageModel(**v) for v in ww_response.data]

        # 批量获取已存在的package_id和emoji_id
        existing_packages = await EmojiPackage.all().values_list(
            "package_id", flat=True
        )
        existing_emojis = await EmojiItem.all().values_list("emoji_id", flat=True)

        existing_packages_set = set(existing_packages)
        existing_emojis_set = set(existing_emojis)

        # 存储表情包数据
        for package_data in emoji_packages:
            if "战双" in package_data.title:
                continue

            if package_data.id in existing_packages_set:
                # 更新现有表情包
                package = await EmojiPackage.get(package_id=package_data.id)
                await package.update_from_dict(
                    {
                        "title": package_data.title,
                        "creat_time": package_data.creat_time,
                        "active_time": package_data.active_time,
                        "update_time": package_data.update_time,
                        "main_img_url": package_data.main_img_url,
                        "state_code": package_data.state_code,
                        "timing_active": package_data.timing_active,
                        "package_size": package_data.package_size,
                        "state": package_data.state,
                    }
                )
            else:
                # 创建新表情包
                package = await EmojiPackage.create(
                    package_id=package_data.id,
                    title=package_data.title,
                    creat_time=package_data.creat_time,
                    active_time=package_data.active_time,
                    update_time=package_data.update_time,
                    main_img_url=package_data.main_img_url,
                    state_code=package_data.state_code,
                    timing_active=package_data.timing_active,
                    package_size=package_data.package_size,
                    state=package_data.state,
                )

            # 存储表情项数据
            for emoji_data in package_data.emoji_list:
                if emoji_data.id in existing_emojis_set:
                    # 更新现有表情项
                    emoji = await EmojiItem.get(emoji_id=emoji_data.id)
                    await emoji.update_from_dict(
                        {
                            "img_url": emoji_data.img_url,
                            "img_size": emoji_data.img_size,
                            "name": emoji_data.name,
                            "package_id": emoji_data.package_id,
                        }
                    )
                else:
                    # 创建新表情项
                    await EmojiItem.create(
                        emoji_id=emoji_data.id,
                        img_url=emoji_data.img_url,
                        img_size=emoji_data.img_size,
                        name=emoji_data.name,
                        package_id=emoji_data.package_id,
                        is_downloaded=False,
                        path="",  # 初始为空，下载后设置
                    )

        return len(emoji_packages)

    @classmethod
    async def download_emojis(cls):
        """下载所有未下载的表情"""
        # 获取所有未下载的表情
        undownloaded_emojis = await EmojiItem.filter(is_downloaded=False).all()

        for emoji in undownloaded_emojis:
            try:
                # 根据packageId创建文件夹
                package_folder = EMOJI_PATH / emoji.package_id
                package_folder.mkdir(parents=True, exist_ok=True)

                # 生成文件名（使用emoji_id和原始扩展名）
                file_extension = Path(emoji.img_url).suffix or ".gif"
                filename = f"{emoji.emoji_id}{file_extension}"
                file_path = package_folder / filename

                if file_path.exists():
                    continue

                # 下载表情图片
                response = await AsyncHttpx.get(emoji.img_url)
                response.raise_for_status()

                # 保存文件
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(response.content)

                # 更新数据库记录
                await emoji.update_from_dict(
                    {"is_downloaded": True, "path": str(file_path)}
                )

                logger.debug(f"成功下载表情: {emoji.name} -> {file_path}", LOG_COMMAND)

            except Exception as e:
                logger.warning(
                    f"下载表情失败 {emoji.name} ({emoji.emoji_id})", LOG_COMMAND, e=e
                )

        return len(undownloaded_emojis)
