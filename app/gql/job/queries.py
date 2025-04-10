import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.gql.types import Job_gql
from app.db.repositories.job_repository import JobRepository


@strawberry.type
class JobQuery:
    @strawberry.field
    def jobs(self, info: Info) -> List[Job_gql]:
        db_session = info.context["db_session"]
        return JobRepository.get_all_jobs(db_session=db_session)

    @strawberry.field
    def job(self, id: int, info: Info) -> Optional[Job_gql]:
        db_session = info.context["db_session"]
        return JobRepository.get_job_by_id(db_session, id)
