import strawberry
from strawberry.types import Info
from typing import List
from .types import (
    Job as Job_gql,
    Employer as Employer_gql,
)
from app.db.database import (
    Employer_sql,
    Job_sql,
)
from sqlalchemy.orm import joinedload
from .utils import to_employer_gql, to_job_gql


@strawberry.type
class Query:
    # Given a job, allow retrieval of all other jobs from this employer.
    @strawberry.field
    def jobs(self, info: Info) -> List[Job_gql]:
        db_session = info.context["db_session"]
        jobs = db_session.query(Job_sql).options(joinedload(Job_sql.employer)).all()
        return [to_job_gql(job, deep=True) for job in jobs]

    # Allow retrieval of an employer's jobs.
    # Disallow retrieval of the employer's jobs' employer
    # (not useful anyway, since a job can't have multiple employers).
    @strawberry.field
    def employers(self, info: Info) -> List[Employer_gql]:
        db_session = info.context["db_session"]
        employers = (
            db_session.query(Employer_sql).options(joinedload(Employer_sql.jobs)).all()
        )
        return [to_employer_gql(employer, deep=True) for employer in employers]

    @strawberry.field
    def job(self, id: int, info: Info) -> Job_gql:
        db_session = info.context["db_session"]
        job = (
            db_session.query(Job_sql)
            .options(joinedload(Job_sql.employer))
            .filter_by(id=id)
            .first()
        )
        return to_job_gql(job, deep=True) if job else None

    @strawberry.field
    def employer(self, id: int, info: Info) -> Employer_gql:
        db_session = info.context["db_session"]
        employer = (
            db_session.query(Employer_sql)
            .options(joinedload(Employer_sql.jobs))
            .filter_by(id=id)
            .first()
        )
        return to_employer_gql(employer, deep=True) if employer else None
