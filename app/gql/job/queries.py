import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.gql.types import (
    Job as Job_gql,
)
from app.db.database import Job_sql
from sqlalchemy.orm import joinedload
from app.gql.utils import to_job_gql


@strawberry.type
class JobQuery:
    # Given a job, allow retrieval of all other jobs from this employer.
    @strawberry.field
    def jobs(self, info: Info) -> List[Job_gql]:
        db_session = info.context["db_session"]
        jobs = db_session.query(Job_sql).options(joinedload(Job_sql.employer)).all()
        return [to_job_gql(job, deep=True) for job in jobs]

    @strawberry.field
    def job(self, id: int, info: Info) -> Optional[Job_gql]:
        db_session = info.context["db_session"]
        job = (
            db_session.query(Job_sql)
            .options(joinedload(Job_sql.employer))
            .filter_by(id=id)
            .first()
        )
        return to_job_gql(job, deep=True) if job else None
