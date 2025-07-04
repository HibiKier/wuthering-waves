import copy

from ...exceptions import WavesException
from ...handles.char import CharHandler
from ...handles.cookie import CookieHandler
from ...models.waves_character import WavesCharacter, WavesWeapon
from ...models.waves_user import WavesUser
from ...utils.manager.entity_manager import EntityManager
from ...utils.resource.constant import SPECIAL_CHAR
from ...waves_api import WavesApi
from ...waves_api.api.online.models import RoleItem, WeaponItem
from ...waves_api.api.other import OtherApi
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_102
from .config import skill_break_list, skill_index_kuro, template_role_develop


class DevelopDataSource:
    @classmethod
    async def calc_develop_cost(
        cls, user_id: str, role_id: str | None, develop_list: tuple[str, ...]
    ):
        if not role_id:
            role_ids = await WavesUser.get_role_ids(user_id)
            if not role_ids:
                raise WavesException("还未绑定任何鸣潮特征码")
            role_id = role_ids[0]
        alias_char_ids = []
        for develop in develop_list:
            char_id = EntityManager.name_to_id(develop)
            if char_id is None:
                continue
            alias_char_ids.append(char_id)
        if not alias_char_ids:
            raise WavesException("未找到养成角色")
        cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(f"{ERROR_CODE[WAVES_CODE_102]}")
        response = await OtherApi.calculator_refresh_data(role_id, cookie)
        if not response.data:
            raise WavesException("养成数据刷新失败  ")
        online_char_map: dict[int, RoleItem] = await CharHandler.get_online_char_map()
        online_weapon_map: dict[
            int, WeaponItem
        ] = await CharHandler.get_online_weapon_map()
        owned_role = (await WavesApi.get_owned_role(role_id, cookie)).data

        owned_characters = []
        unowned_characters = []
        for char_id in alias_char_ids:
            if char_id not in online_char_map:
                continue
            if char_id in SPECIAL_CHAR:
                find_char_ids = SPECIAL_CHAR[char_id]
                for find_char_id in find_char_ids:
                    if find_char_id in owned_role:
                        char_id = find_char_id
                        break
            if char_id in owned_role:
                owned_characters.append(char_id)
            else:
                unowned_characters.append(char_id)

        develop_data_map = {}
        if owned_characters:
            develop_data = await WavesApi.get_develop_role_cultivate_status(
                role_id, cookie, owned_characters
            )
            develop_data_map = {item.role_id: item for item in develop_data.data}

        waves_data = await WavesCharacter.get_chars(role_id)
        if not waves_data:
            # 尝试刷新
            await CharHandler.refresh_char(user_id, role_id, cookie, is_self)
            waves_data = await WavesCharacter.get_chars(role_id)

        content_list = []
        for no_owned_char_id in unowned_characters:
            template_role = copy.deepcopy(template_role_develop)
            template_role["roleId"] = no_owned_char_id

            char_name = EntityManager.id_to_name(no_owned_char_id)
            if char_name:
                weapon_id = EntityManager.get_weapon_alias(f"{char_name}专武")
                if weapon_id:
                    template_role["weaponId"] = EntityManager.name_to_id(weapon_id)

            content_list.append(template_role)

        for char in waves_data:
            char_id = int(char.character_base.char_id)
            if char_id not in develop_data_map:
                continue
            develop_data = develop_data_map[char_id]
            template_role = copy.deepcopy(template_role_develop)
            template_role["roleId"] = char_id
            template_role["roleStartLevel"] = develop_data.role_level

            for skill in develop_data.skill_level_list:
                skill_index = skill_index_kuro[skill.type]
                if skill.type == "其他技能" or skill.type == "延奏技能":
                    continue

                template_role["skillLevelUpList"][skill_index]["startLevel"] = (
                    skill.level
                )
            weapon: WavesWeapon | None = getattr(char, "weapon", None)
            if weapon:
                template_role["weaponId"] = weapon.weapon_detail.weapon_id
                template_role["weaponStartLevel"] = (
                    weapon.weapon_detail.weapon_star_level
                )
                template_role["advanceSkillList"] = list(
                    set(skill_break_list).difference(set(develop_data.skill_break_list))
                )
                content_list.append(template_role)

        if not content_list:
            raise WavesException("未找到养成角色")
