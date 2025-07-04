from ...exceptions import WavesException
from ...handles.char import CharHandler
from ...handles.cookie import CookieHandler
from ...models.waves_character import WavesCharacter
from ...models.waves_user import WavesUser
from ...waves_api.error_code import ERROR_CODE, WAVES_CODE_100, WAVES_CODE_102


class CharListDataSource:
    @classmethod
    async def get_char_list(cls, user_id: str, role_id: str | None = None):
        if not role_id:
            role_ids = await WavesUser.get_role_ids(user_id)
            if not role_ids:
                raise WavesException(ERROR_CODE[WAVES_CODE_100])
            role_id = role_ids[0]
        cookie, is_self = await CookieHandler.get_cookie(user_id, role_id)
        if not cookie:
            raise WavesException(ERROR_CODE[WAVES_CODE_102])
        # account_info = (await WavesApi.get_base_info(role_id, cookie)).data

        chars = await WavesCharacter.get_chars(role_id)
        # if not chars:
        # 尝试刷新
        await CharHandler.refresh_char(user_id, role_id, cookie, is_self)
        chars = await WavesCharacter.get_chars(role_id)
        if not chars:
            raise WavesException("练度获取失败，请先刷新角色面板")
        print()
