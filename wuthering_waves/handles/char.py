import asyncio

from aiocache import cached

from ..base_models import WwBaseResponse
from ..exceptions import WavesException
from ..handles.cookie import CookieHandler
from ..models.waves_character import (
    WavesChain,
    WavesCharacter,
    WavesCharacterBase,
    WavesCharChain,
    WavesCharSkill,
    WavesFetterDetail,
    WavesPhantom,
    WavesPhantomProps,
    WavesProps,
    WavesSkill,
    WavesWeapon,
    WavesWeaponDetail,
)
from ..utils.utils import with_semaphore
from ..waves_api import WavesApi
from ..waves_api.api.online.models import RoleItem, WeaponItem
from ..waves_api.api.role.models import CharDetailData
from ..waves_api.error_code import ERROR_CODE, WAVES_CODE_101, WAVES_CODE_102


class CharHandler:
    @classmethod
    async def is_online_char(cls, user_id: str, role_id: str, char_id: int) -> bool:
        """检查角色是否是已上线角色

        参数:
            user_id: 用户ID
            role_id: 角色（用户）ID
            char_id: 角色ID

        返回:
            bool: 角色是否在线

        异常:
            WavesException: 获取角色信息失败
        """
        cookie, _ = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        online_list = await WavesApi.get_online_list_role(cookie)
        return char_id in [r.role_id for r in online_list.data]

    @classmethod
    async def refresh_char(
        cls,
        user_id: str,
        role_id: str,
        cookie: str | None = None,
        is_self: bool = False,
        refresh_chars: list[int] | str = "all",
    ) -> tuple[list[CharDetailData], list[int], list[int]]:
        """刷新角色数据

        参数:
            user_id: 用户ID
            role_id: 角色（用户）ID
            cookie: 登录cookie
            is_self: 是否为自身cookie
            refresh_chars: 刷新角色列表，列表内为角色id

        异常:
            WavesException: 获取角色信息失败
            WavesException: 获取角色数据失败
            WavesException: 库街区暂未查询到角色数据

        返回:
            tuple[list[CharDetailData], list[int], list[int]]: 角色数据列表、
                变化的角色ID列表和未变化的角色ID列表
        """
        if not cookie:
            cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        role_info = await WavesApi.get_role_info(role_id, cookie)
        char_list = role_info.data.role_list
        if not is_self:
            char_list = role_info.data.show_role_id_list
        else:
            char_list = [r.role_id for r in char_list]
        if not char_list:
            raise WavesException("当前角色列表为空")
        if isinstance(refresh_chars, list):
            char_list = [r for r in char_list if r in refresh_chars]
        semaphore = asyncio.Semaphore(value=2)
        tasks = [
            with_semaphore(
                semaphore,
                WavesApi.get_char_detail_info,
                char_id=char_id,
                role_id=role_id,
                cookie=cookie,
            )
            for char_id in char_list
        ]
        results: list[WwBaseResponse[CharDetailData] | None] = await asyncio.gather(
            *tasks
        )

        char_list = [r.data.role for r in results if r]
        if not char_list:
            if refresh_chars == "all":
                raise WavesException(ERROR_CODE[WAVES_CODE_101])
            else:
                raise WavesException("库街区暂未查询到角色数据")

        # 检查数据变化
        changed_chars, unchanged_chars = await cls.check_data_changes(
            role_id, [r.data for r in results if r]
        )

        # 保存获取到的角色数据
        for result in results:
            if result and result.data:
                await cls._save_char_data(role_id, result.data)

        return [r.data for r in results if r], changed_chars, unchanged_chars

    @classmethod
    async def check_data_changes(
        cls, role_id: str, char_data_list: list[CharDetailData]
    ) -> tuple[list[int], list[int]]:  # sourcery skip: hoist-if-from-if
        """检查角色数据变化

        参数:
            char_data_list: 角色详细数据列表

        返回:
            Tuple[List[int], List[int]]: 变化的角色ID列表和未变化的角色ID列表
        """
        changed_chars = []
        unchanged_chars = []

        db_chars = await WavesCharacter.get_chars(role_id)

        for char_data in char_data_list:
            char_id = char_data.role.role_id
            has_changes = False

            # 获取数据库中的角色信息
            db_char = next(
                (c for c in db_chars if c.character_base.char_id == char_id), None
            )
            if not db_char:
                # 新角色，直接添加到变化列表
                changed_chars.append(char_id)
                continue

            # 检查角色基本信息变化
            if (
                db_char.level != char_data.role.level
                or db_char.breach != char_data.role.breach
                or db_char.chain_unlock_num != char_data.role.chain_unlock_num
            ):
                has_changes = True

            # 检查技能变化
            if not has_changes:
                # 获取数据库中的技能信息
                db_skills = await WavesCharSkill.filter(
                    character_id=db_char.id
                ).prefetch_related("skill")
                db_skill_ids = {rs.skill.skill_id: rs.level for rs in db_skills}

                # 获取API返回的技能信息
                api_skill_ids = {
                    skill_item.skill.id: skill_item.level
                    for skill_item in char_data.skill_list
                }

                # 比较技能ID和等级
                if set(db_skill_ids.keys()) != set(api_skill_ids.keys()):
                    has_changes = True
                else:
                    # 比较技能等级
                    for skill_id, level in api_skill_ids.items():
                        if skill_id in db_skill_ids and db_skill_ids[skill_id] != level:
                            has_changes = True
                            break

            # 检查链变化
            if not has_changes:
                # 获取数据库中的链信息
                db_chains = await WavesCharChain.filter(
                    character_id=db_char.id
                ).prefetch_related("chain")
                db_chain_names = {rc.chain.name for rc in db_chains if rc.chain.name}

                # 获取API返回的链信息
                api_chain_names = {
                    chain.name for chain in char_data.chain_list if chain.name
                }

                # 比较链名称
                if db_chain_names != api_chain_names:
                    has_changes = True

            # 检查武器变化
            if not has_changes:
                weapon = await WavesWeapon.filter(character_id=db_char.id).first()
                if weapon:
                    if (
                        weapon.level != char_data.weapon_data.level
                        or weapon.breach != char_data.weapon_data.breach
                        or weapon.reson_level != char_data.weapon_data.reson_level
                    ):
                        has_changes = True

                    # 检查武器类型是否变化
                    if not has_changes:
                        weapon_detail = await weapon.weapon_detail
                        if (
                            weapon_detail.weapon_id
                            != char_data.weapon_data.weapon.weapon_id
                        ):
                            has_changes = True
                else:
                    # 没有武器记录但现在有武器数据，认为有变化
                    has_changes = True

            # 检查声骇装备变化
            if not has_changes:
                db_phantoms = await WavesPhantom.filter(
                    character_id=db_char.id
                ).prefetch_related("fetter_detail")
                db_phantom_ids = {p.fetter_detail.group_id for p in db_phantoms}

                # 获取新的声骇装备组ID
                new_phantom_ids = {
                    ep.fetter_detail.group_id
                    for ep in char_data.phantom_data.equip_phantom_list
                    if ep
                }

                # 检查是否有新增或移除的声骇装备
                added_phantoms = new_phantom_ids - db_phantom_ids
                removed_phantoms = db_phantom_ids - new_phantom_ids

                if added_phantoms or removed_phantoms:
                    has_changes = True

                # 检查共同的声骇装备是否有变化
                if not has_changes:
                    common_phantoms = db_phantom_ids & new_phantom_ids

                    for group_id in common_phantoms:
                        db_phantom = next(
                            (
                                p
                                for p in db_phantoms
                                if p.fetter_detail.group_id == group_id
                            ),
                            None,
                        )
                        new_phantom = next(
                            (
                                p
                                for p in char_data.phantom_data.equip_phantom_list
                                if p and p.fetter_detail.group_id == group_id
                            ),
                            None,
                        )

                        if (
                            db_phantom
                            and new_phantom
                            and (
                                db_phantom.level != new_phantom.level
                                or db_phantom.quality != new_phantom.quality
                            )
                        ):
                            has_changes = True
                            break

            # 根据是否有变化，添加到相应的列表
            if has_changes:
                changed_chars.append(char_id)
            else:
                unchanged_chars.append(char_id)

        return changed_chars, unchanged_chars

    @classmethod
    async def get_char_skills(
        cls, role_id: str, char_id: int
    ) -> list[tuple[WavesSkill, int]]:
        """获取角色的技能列表

        参数:
            role_id: 角色（用户）ID
            char_id: 角色ID

        返回:
            List[Tuple[WavesSkill, int]]: 技能列表和等级
        """
        # 先获取角色基础信息
        char_base = await WavesCharacterBase.filter(char_id=char_id).first()
        if not char_base:
            return []

        # 再获取用户特定的角色数据
        char = await WavesCharacter.filter(
            role_id=role_id, character_base=char_base
        ).first()
        if not char:
            return []

        # 获取角色的所有技能关联
        char_skills = await WavesCharSkill.filter(
            character_id=char.id
        ).prefetch_related("skill")
        return [(cs.skill, cs.level) for cs in char_skills]

    @classmethod
    async def get_char_chains(cls, role_id: str, char_id: int) -> list[WavesChain]:
        """获取角色的链列表

        参数:
            role_id: 角色（用户）ID
            char_id: 角色ID

        返回:
            List[WavesChain]: 链列表
        """
        # 先获取角色基础信息
        char_base = await WavesCharacterBase.filter(char_id=char_id).first()
        if not char_base:
            return []

        # 直接从角色基础信息获取链列表
        return await WavesChain.filter(character_base=char_base).all()

    @classmethod
    async def _save_char_data(cls, role_id: str, char_data: CharDetailData):
        """保存角色数据到数据库

        参数:
            role_id: 角色（用户）ID
            char_data: 角色详细数据
        """
        # 1. 保存角色基础信息
        char_data_role = char_data.role

        # 先创建或更新角色基础信息
        char_base, _ = await WavesCharacterBase.get_or_create(
            char_id=char_data_role.role_id,
            defaults={
                "char_name": char_data_role.role_name,
                "char_icon_url": char_data_role.role_icon_url,
                "char_pic_url": char_data_role.role_pic_url,
                "star_level": char_data_role.star_level,
                "attribute_id": char_data_role.attribute_id,
                "attribute_name": char_data_role.attribute_name,
                "weapon_type_id": char_data_role.weapon_type_id,
                "weapon_type_name": char_data_role.weapon_type_name,
                "acronym": char_data_role.acronym,
            },
        )

        # 创建或更新用户特定的角色数据
        char, _ = await WavesCharacter.get_or_create(
            role_id=role_id,
            character_base=char_base,
            defaults={
                "level": char_data_role.level,
                "breach": char_data_role.breach,
                "chain_unlock_num": char_data_role.chain_unlock_num,
            },
        )

        # 如果用户特定数据已存在，更新相关字段
        if not _:
            char.level = char_data_role.level
            char.breach = char_data_role.breach
            char.chain_unlock_num = char_data_role.chain_unlock_num
            await char.save()

        # 2. 保存技能信息
        # 删除该角色之前的技能关联
        await WavesCharSkill.filter(character_id=char.id).delete()

        for skill_item in char_data.skill_list:
            skill_data = skill_item.skill
            skill, _ = await WavesSkill.get_or_create(
                skill_id=skill_data.id,
                defaults={
                    "type": skill_data.type,
                    "name": skill_data.name,
                    "description": skill_data.description,
                    "icon_url": skill_data.icon_url,
                },
            )

            # 创建角色与技能的关联
            await WavesCharSkill.create(
                character=char, skill=skill, level=skill_item.level
            )

        # 3. 保存链信息
        # 删除该角色之前的链关联
        await WavesCharChain.filter(character_id=char.id).delete()

        for chain_data in char_data.chain_list:
            chain, _ = await WavesChain.get_or_create(
                character_base=char_base,
                name=chain_data.name,
                order=chain_data.order,
                defaults={
                    "description": chain_data.description,
                    "icon_url": chain_data.icon_url,
                },
            )

            # 创建角色与链的关联
            await WavesCharChain.create(character=char, chain=chain, is_unlocked=True)

        # 4. 保存武器信息
        weapon_data = char_data.weapon_data.weapon
        weapon_detail, _ = await WavesWeaponDetail.get_or_create(
            weapon_id=weapon_data.weapon_id,
            defaults={
                "weapon_name": weapon_data.weapon_name,
                "weapon_type": weapon_data.weapon_type,
                "weapon_star_level": weapon_data.weapon_star_level,
                "weapon_icon": weapon_data.weapon_icon,
                "weapon_effect_name": weapon_data.weapon_effect_name,
            },
        )

        # 删除该角色之前的武器关联（一个角色只有一个武器）
        await WavesWeapon.filter(character_id=char.id).delete()

        # 创建新的武器关联
        await WavesWeapon.create(
            character=char,
            weapon_detail=weapon_detail,
            level=char_data.weapon_data.level,
            breach=char_data.weapon_data.breach,
            reson_level=char_data.weapon_data.reson_level,
        )

        # 5. 保存声骇装备信息（一个角色最多有5个声骇装备）
        # 首先删除该角色之前的声骇装备
        phantoms = await WavesPhantom.filter(character_id=char.id)
        await WavesPhantomProps.filter(phantom_id__in=[p.id for p in phantoms]).delete()
        await WavesPhantom.filter(character_id=char.id).delete()

        # 保存新的声骇装备
        for equip_phantom in char_data.phantom_data.equip_phantom_list:
            if not equip_phantom:
                continue
            # 保存羁绊信息
            fetter_data = equip_phantom.fetter_detail
            fetter, _ = await WavesFetterDetail.get_or_create(
                group_id=fetter_data.group_id,
                name=fetter_data.name,
                num=fetter_data.num,
                defaults={
                    "icon_url": fetter_data.icon_url,
                    "first_description": fetter_data.first_description,
                    "second_description": fetter_data.second_description,
                },
            )

            # 创建声骇装备
            phantom = await WavesPhantom.create(
                character=char,
                cost=equip_phantom.cost,
                quality=equip_phantom.quality,
                level=equip_phantom.level,
                fetter_detail=fetter,
            )

            # 保存主属性
            for main_prop in equip_phantom.main_props:
                if main_prop.valid:
                    prop, _ = await WavesProps.get_or_create(
                        attribute_name=main_prop.attribute_name,
                        attribute_value=main_prop.attribute_value,
                        defaults={"icon_url": main_prop.icon_url},
                    )
                    await WavesPhantomProps.create(
                        phantom=phantom, props=prop, is_main=True
                    )

            # 保存副属性
            for sub_prop in equip_phantom.sub_props:
                if sub_prop.valid:
                    prop, _ = await WavesProps.get_or_create(
                        attribute_name=sub_prop.attribute_name,
                        attribute_value=sub_prop.attribute_value,
                        defaults={"icon_url": None},
                    )
                    await WavesPhantomProps.create(
                        phantom=phantom, props=prop, is_main=False
                    )

    @classmethod
    @cached(ttl=60 * 60 * 24)
    async def get_online_char_map(cls) -> dict[int, RoleItem]:
        """获取已上线的角色列表"""
        cookie = await CookieHandler.get_random_cookie()
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        online_list: WwBaseResponse[
            list[RoleItem]
        ] = await WavesApi.get_online_list_role(cookie)
        return {r.role_id: r for r in online_list.data}

    @classmethod
    @cached(ttl=60 * 60 * 6)
    async def get_online_weapon_map(cls) -> dict[int, WeaponItem]:
        """获取已上线的武器列表"""
        cookie = await CookieHandler.get_random_cookie()
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        online_list: WwBaseResponse[
            list[WeaponItem]
        ] = await WavesApi.get_online_list_weapon(cookie)
        return {r.weapon_id: r for r in online_list.data}
