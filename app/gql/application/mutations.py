import strawberry
from strawberry.types import Info
from app.auth.roles import Role
from app.auth.auth_utils import require_role
from app.db.repositories.application_repository import ApplicationRepository


@strawberry.type
class ApplicationMutation:
    @strawberry.mutation
    @require_role([Role.USER])
    def apply_to_job(self, job_id: int, info: Info) -> bool:
        user = info.context["user"]
        db_session = info.context["db_session"]

        return ApplicationRepository.create_application(
            db_session=db_session, user_id=user.id, job_id=job_id
        )
