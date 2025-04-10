import strawberry
from typing import List
from strawberry.types import Info
from app.gql.types import User_gql
from app.auth.auth_utils import require_role
from app.auth.roles import Role
from app.db.repositories.user_repository import UserRepository


@strawberry.type
class UserQuery:

    @strawberry.field
    @require_role([Role.ADMIN, Role.USER])
    def users(self, info: Info) -> List[User_gql]:
        db_session = info.context["db_session"]
        user = info.context.get("user", None)

        if user.role == Role.ADMIN:
            return UserRepository.get_all_users(db_session, gql=True)
        elif user.role == Role.USER:
            user = UserRepository.get_user_by_id(db_session, id=user.id)
            return [user] if user is not None else []
        return []
