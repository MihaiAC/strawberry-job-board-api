import strawberry
from strawberry.types import Info
from app.db.models import Job_gql
from typing import Optional
from app.auth.roles import Role
from app.auth.auth_utils import require_role
from app.db.repositories.job_repository import JobRepository

from sqlalchemy.orm import Session


@strawberry.type
class JobMutation:
    @strawberry.mutation
    @require_role([Role.ADMIN])
    def add_job(
        self,
        title: str,
        description: str,
        employer_id: int,
        info: Info,
    ) -> Job_gql:
        db_session = info.context["db_session"]
        return JobRepository.add_job(
            db_session=db_session,
            title=title,
            description=description,
            employer_id=employer_id,
        )

    @strawberry.mutation
    @require_role([Role.ADMIN])
    def update_job(
        self,
        job_id: int,
        info: Info,
        title: Optional[str] = None,
        description: Optional[str] = None,
        employer_id: Optional[int] = None,
    ) -> Job_gql:
        """
        At least one of title, description, employer_id should be provided.
        Throws error if no job with the given id has been found.
        """
        db_session = info.context["db_session"]
        return JobRepository.update_job(
            db_session=db_session,
            job_id=job_id,
            title=title,
            description=description,
            employer_id=employer_id,
        )

    @strawberry.mutation
    @require_role([Role.ADMIN])
    def delete_job(
        self,
        job_id: int,
        info: Info,
    ) -> bool:
        db_session: Session = info.context["db_session"]
        return JobRepository.delete_job(db_session=db_session, job_id=job_id)
