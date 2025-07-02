import asyncio

from ..base_models import WwBaseResponse
from ..exceptions import WavesException
from ..handles.cookie import CookieHandler
from ..models.role import (
    Chain,
    FetterDetail,
    Phantom,
    PhantomProps,
    Props,
    Role,
    Skill,
    Weapon,
    WeaponDetail,
)
from ..utils.utils import with_semaphore
from ..waves_api import WavesApi
from ..waves_api.api.role.models import CharDetailData
from ..waves_api.error_code import ERROR_CODE, WAVES_CODE_101, WAVES_CODE_102


class RoleHandler:
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
        changed_roles, unchanged_roles = await cls.check_data_changes(
            [r.data for r in results if r]
        )

        # 保存获取到的角色数据
        for result in results:
            if result and result.data:
                await cls._save_char_data(result.data)

        return [r.data for r in results if r], changed_roles, unchanged_roles

    @classmethod
    async def check_data_changes(
        cls, char_data_list: list[CharDetailData]
    ) -> tuple[list[int], list[int]]:
        """检查角色数据变化

        参数:
            char_data_list: 角色详细数据列表

        返回:
            Tuple[List[int], List[int]]: 变化的角色ID列表和未变化的角色ID列表
        """
        changed_roles = []
        unchanged_roles = []

        for char_data in char_data_list:
            role_id = char_data.role.role_id
            has_changes = False

            # 获取数据库中的角色信息
            db_role = await Role.filter(role_id=role_id).first()
            if not db_role:
                # 新角色，直接添加到变化列表
                changed_roles.append(role_id)
                continue

            # 检查角色基本信息变化
            if (
                db_role.level != char_data.role.level
                or db_role.breach != char_data.role.breach
                or db_role.chain_unlock_num != char_data.role.chain_unlock_num
            ):
                has_changes = True

            # 检查武器变化
            if not has_changes:
                weapon = await Weapon.filter(role_id=db_role.id).first()
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
                db_phantoms = await Phantom.filter(role_id=db_role.id).prefetch_related(
                    "fetter_detail"
                )
                db_phantom_ids = {p.fetter_detail.group_id for p in db_phantoms}

                # 获取新的声骇装备组ID
                new_phantom_ids = {
                    ep.fetter_detail.group_id
                    for ep in char_data.phantom_data.equip_phantom_list
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
                                if p.fetter_detail.group_id == group_id
                            ),
                            None,
                        )

                        if db_phantom and new_phantom:
                            if (
                                db_phantom.level != new_phantom.level
                                or db_phantom.quality != new_phantom.quality
                            ):
                                has_changes = True
                                break

            # 根据是否有变化，添加到相应的列表
            if has_changes:
                changed_roles.append(role_id)
            else:
                unchanged_roles.append(role_id)

        return changed_roles, unchanged_roles

    @classmethod
    async def _save_char_data(cls, char_data: CharDetailData):
        """保存角色数据到数据库

        参数:
            char_data: 角色详细数据
        """
        # 1. 保存角色基础信息
        role_data = char_data.role
        role, _ = await Role.get_or_create(
            role_id=role_data.role_id,
            defaults={
                "level": role_data.level,
                "breach": role_data.breach,
                "role_name": role_data.role_name,
                "role_icon_url": role_data.role_icon_url,
                "role_pic_url": role_data.role_pic_url,
                "star_level": role_data.star_level,
                "attribute_id": role_data.attribute_id,
                "attribute_name": role_data.attribute_name,
                "weapon_type_id": role_data.weapon_type_id,
                "weapon_type_name": role_data.weapon_type_name,
                "acronym": role_data.acronym,
                "chain_unlock_num": role_data.chain_unlock_num,
            },
        )

        # 更新角色信息（如果已存在）
        if not _:
            # 如果角色已存在，更新相关信息
            role.level = role_data.level
            role.breach = role_data.breach
            role.role_name = role_data.role_name
            role.role_icon_url = role_data.role_icon_url
            role.role_pic_url = role_data.role_pic_url
            role.star_level = role_data.star_level
            role.attribute_id = role_data.attribute_id
            role.attribute_name = role_data.attribute_name
            role.weapon_type_id = role_data.weapon_type_id
            role.weapon_type_name = role_data.weapon_type_name
            role.acronym = role_data.acronym
            role.chain_unlock_num = role_data.chain_unlock_num
            await role.save()

        # 2. 保存技能信息
        for skill_item in char_data.skill_list:
            skill_data = skill_item.skill
            skill, _ = await Skill.get_or_create(
                skill_id=skill_data.id,
                defaults={
                    "type": skill_data.type,
                    "name": skill_data.name,
                    "description": skill_data.description,
                    "icon_url": skill_data.icon_url,
                },
            )

        # 3. 保存链信息
        for chain_data in char_data.chain_list:
            chain, _ = await Chain.get_or_create(
                name=chain_data.name,
                order=chain_data.order,
                defaults={
                    "description": chain_data.description,
                    "icon_url": chain_data.icon_url,
                },
            )

        # 4. 保存武器信息
        weapon_data = char_data.weapon_data.weapon
        weapon_detail, _ = await WeaponDetail.get_or_create(
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
        await Weapon.filter(role_id=role.id).delete()

        # 创建新的武器关联
        await Weapon.create(
            role=role,
            weapon_detail=weapon_detail,
            level=char_data.weapon_data.level,
            breach=char_data.weapon_data.breach,
            reson_level=char_data.weapon_data.reson_level,
        )

        # 5. 保存声骇装备信息（一个角色最多有5个声骇装备）
        # 首先删除该角色之前的声骇装备
        phantoms = await Phantom.filter(role_id=role.id)
        await PhantomProps.filter(phantom_id__in=[p.id for p in phantoms]).delete()
        await Phantom.filter(role_id=role.id).delete()

        # 保存新的声骇装备
        for equip_phantom in char_data.phantom_data.equip_phantom_list:
            # 保存羁绊信息
            fetter_data = equip_phantom.fetter_detail
            fetter, _ = await FetterDetail.get_or_create(
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
            phantom = await Phantom.create(
                role=role,
                cost=equip_phantom.cost,
                quality=equip_phantom.quality,
                level=equip_phantom.level,
                fetter_detail=fetter,
            )

            # 保存主属性
            for main_prop in equip_phantom.main_props:
                if main_prop.valid:
                    prop, _ = await Props.get_or_create(
                        attribute_name=main_prop.attribute_name,
                        attribute_value=main_prop.attribute_value,
                        defaults={"icon_url": main_prop.icon_url},
                    )
                    await PhantomProps.create(phantom=phantom, props=prop, is_main=True)

            # 保存副属性
            for sub_prop in equip_phantom.sub_props:
                if sub_prop.valid:
                    prop, _ = await Props.get_or_create(
                        attribute_name=sub_prop.attribute_name,
                        attribute_value=sub_prop.attribute_value,
                        defaults={"icon_url": None},
                    )
                    await PhantomProps.create(
                        phantom=phantom, props=prop, is_main=False
                    )
