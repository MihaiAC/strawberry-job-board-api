import strawberry
from strawberry.types import Info
from .types import (
    Job as Job_gql,
    Success as Success_gql,
)
from app.db.database import Job_sql
from .utils import to_employer_gql, to_job_gql


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_job(
        self,
        title: str,
        description: str,
        employer_id: int,
        info: Info,
    ) -> Job_gql:
        db_session = info.context["db_session"]
        job_sql = Job_sql(title=title, description=description, employer_id=employer_id)
        db_session.add(job_sql)
        db_session.commit()
        db_session.refresh(job_sql)

        job_gql = to_job_gql(job_sql, deep=True)
        return job_gql

    # def update_job
