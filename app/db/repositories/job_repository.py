from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Job as Job_sql
from app.gql.types import Job_gql
from app.errors.custom_errors import ResourceNotFound
from app.sql_to_gql import job_to_gql


class JobRepository:
    @staticmethod
    def get_all_jobs(db_session: Session, gql: bool = False) -> List[Job_gql | Job_sql]:
        jobs = Job_sql.get_all(db_session)
        if gql:
            return [job_to_gql(job) for job in jobs]
        return jobs

    @staticmethod
    def get_job_by_id(
        db_session: Session,
        id: int,
        gql: bool = False,
    ) -> Optional[Job_gql | Job_sql]:
        jobs = Job_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"id": id},
        )

        if len(jobs) == 0:
            return None
        elif gql:
            return job_to_gql(jobs[0])
        return jobs[0]

    @staticmethod
    def add_job(
        db_session: Session, title: str, description: str, employer_id: int
    ) -> Job_gql:
        job_sql = Job_sql(title=title, description=description, employer_id=employer_id)
        db_session.add(job_sql)
        db_session.commit()
        db_session.refresh(job_sql)

        return job_to_gql(job_sql)

    @staticmethod
    def update_job(
        db_session: Session,
        job_id: int,
        title: str,
        description: str,
        employer_id: int,
    ):
        # Retrieve the job object.
        job_sql = JobRepository.get_job_by_id(
            db_session=db_session,
            id=job_id,
            gql=False,
        )

        if not job_sql:
            raise ResourceNotFound("Job")

        if title is not None:
            job_sql.title = title

        if description is not None:
            job_sql.description = description

        if employer_id is not None:
            job_sql.employer_id = employer_id

        db_session.commit()
        db_session.refresh(job_sql)
        return job_to_gql(job_sql)

    @staticmethod
    def delete_job(db_session: Session, job_id: int) -> bool:
        job_sql = JobRepository.get_job_by_id(
            db_session,
            id=job_id,
            gql=False,
        )

        if not job_sql:
            raise ResourceNotFound("Job")

        db_session.delete(job_sql)
        db_session.commit()

        return True

    @staticmethod
    def get_jobs_by_employer_ids(
        db_session: Session, employer_ids: List[int]
    ) -> List[Job_sql]:
        return Job_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"employer_id": employer_ids},
        )
