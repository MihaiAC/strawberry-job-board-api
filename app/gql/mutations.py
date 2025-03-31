import strawberry
from strawberry.types import Info
from .types import (
    Job as Job_gql,
    Success as Success_gql,
)
from app.db.database import Job_sql
from .utils import to_employer_gql, to_job_gql
from typing import Optional


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

    @strawberry.mutation
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
        # Validate inputs.
        if title is None and description is None and employer_id is None:
            raise Exception(
                "Please provide at least one job field you would like to modify."
            )

        db_session = info.context["db_session"]

        # Retrieve the job object.
        job_sql = db_session.query(Job_sql).filter(Job_sql.id == job_id).first()
        if not job_sql:
            raise Exception("Job not found")

        if title is not None:
            job_sql.title = title

        if description is not None:
            job_sql.description = description

        if employer_id is not None:
            job_sql.employer_id = employer_id

        db_session.commit()
        db_session.refresh(job_sql)
        return to_job_gql(job_sql, deep=True)

    @strawberry.mutation
    def delete_job(
        self,
        job_id: int,
        info: Info,
    ) -> bool:

        db_session = info.context["db_session"]
        job_sql = db_session.query(Job_sql).filter(Job_sql.id == job_id).first()

        if not job_sql:
            raise Exception("Job not found")

        db_session.delete(job_sql)
        db_session.commit()

        return True
