from zhenxun.builtin_plugins.wuthering_waves.models.role import Role


class RoleHandler:
    @classmethod
    async def get_role(cls, user_id: str, role_id: str) -> Role:
        return await Role.get_or_create(user_id=user_id, role_id=role_id)