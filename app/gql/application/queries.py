import strawberry
from typing import List
from strawberry.types import Info
from app.gql.types import Application_gql
from app.auth.auth_utils import require_role
from app.auth.roles import Role
from app.db.repositories.application_repository import ApplicationRepository


@strawberry.type
class ApplicationQuery:
    @strawberry.field
    @require_role([Role.USER, Role.ADMIN])
    def applications(self, info: Info) -> List[Application_gql]:
        user = info.context["user"]
        db_session = info.context["db_session"]

        if user.role == Role.ADMIN:
            return ApplicationRepository.get_all_applications(db_session, gql=True)
        else:
            return ApplicationRepository.get_all_applications_by_user_id(
                db_session, user.id, gql=True
            )
