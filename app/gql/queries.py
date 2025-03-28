import strawberry
from typing import List
from .types import (
    Job as Job_gql,
    Employer as Employer_gql,
)
from app.db.database import (
    engine,
    Employer_sql,
    Job_sql,
)
from sqlalchemy.orm import Session, joinedload
from .utils import to_employer_gql, to_job_gql


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str) -> str:
        return f"Hello {name}"

    # Given a job, allow retrieval of all other jobs from this employer.
    @strawberry.field
    def jobs(self) -> List[Job_gql]:
        with Session(engine) as session:
            jobs = session.query(Job_sql).options(joinedload(Job_sql.employer)).all()
            return [to_job_gql(job, deep=True) for job in jobs]

    # Allow retrieval of an employer's jobs.
    # Disallow retrieval of the employer's jobs' employer
    # (not useful anyway, since a job can't have multiple employers).
    @strawberry.field
    def employers(self) -> List[Employer_gql]:
        with Session(engine) as session:
            employers = (
                session.query(Employer_sql).options(joinedload(Employer_sql.jobs)).all()
            )
            return [to_employer_gql(employer, deep=True) for employer in employers]

    @strawberry.field
    def job(self, id: int) -> Job_gql:
        with Session(engine) as session:
            job = (
                session.query(Job_sql)
                .options(joinedload(Job_sql.employer))
                .filter_by(id=id)
                .first()
            )
            return to_job_gql(job, deep=True) if job else None

    @strawberry.field
    def employer(self, id: int) -> Employer_gql:
        with Session(engine) as session:
            employer = (
                session.query(Employer_sql)
                .options(joinedload(Employer_gql.jobs))
                .filter_by(id=id)
                .first()
            )
            return to_employer_gql(employer, deep=True) if employer else None
