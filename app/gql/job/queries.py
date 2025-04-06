import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.db.models import Job_gql
from app.auth.auth_utils import require_role
from app.auth.roles import Role
from app.db.repositories.job_repository import JobRepository


@strawberry.type
class JobQuery:
    @strawberry.field
    @require_role([Role.ADMIN, Role.UNAUTHENTICATED, Role.USER])
    def jobs(self, info: Info) -> List[Job_gql]:
        db_session = info.context["db_session"]
        selected_fields = str(info.selected_fields)
        user = info.context.get("user", None)

        if user is None:
            return JobRepository.get_all_jobs_unauth(db_session, selected_fields)
        elif user.role == Role.USER:
            return JobRepository.get_all_jobs_user(db_session, selected_fields, user.id)
        elif user.role == Role.ADMIN:
            return JobRepository.get_all_jobs_admin(db_session, selected_fields)
        return []

    @strawberry.field
    def job(self, id: int, info: Info) -> Optional[Job_gql]:
        db_session = info.context["db_session"]
        selected_fields = str(info.selected_fields)

        return JobRepository.get_job_by_id(db_session, selected_fields, id)
