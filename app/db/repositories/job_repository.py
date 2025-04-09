from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Job as Job_sql
from app.gql.types import Job_gql
from app.errors.custom_errors import ResourceNotFound


class JobRepository:
    @staticmethod
    def get_all_jobs_admin(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[Job_gql | Job_sql]:
        return Job_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_all_jobs_user(
        db_session: Session, selected_fields: str, user_id: int, gql: bool = True
    ) -> List[Job_gql | Job_sql]:
        return Job_sql.get_all(
            db_session=db_session,
            selected_fields=selected_fields,
            gql=gql,
            filter_by_attrs={"user_id": user_id},
        )

    @staticmethod
    def get_all_jobs_unauth(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[Job_gql | Job_sql]:
        return Job_sql.get_all(
            db_session, selected_fields, gql, ignore_fields=["applications"]
        )

    # If you get job by id, no applications join.
    @staticmethod
    def get_job_by_id(
        db_session: Session,
        selected_fields: str,
        id: int,
        gql: bool = True,
    ) -> Optional[Job_gql | Job_sql]:
        jobs = Job_sql.get_all(
            db_session=db_session,
            selected_fields=selected_fields,
            filter_by_attrs={"id": id},
            ignore_fields=["applications"],
            gql=gql,
        )

        return jobs[0] if len(jobs) > 0 else None

    @staticmethod
    def add_job(
        db_session: Session, title: str, description: str, employer_id: int
    ) -> Job_gql:
        job_sql = Job_sql(title=title, description=description, employer_id=employer_id)
        db_session.add(job_sql)
        db_session.commit()
        db_session.refresh(job_sql)

        return job_sql.to_gql()

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
            selected_fields="",
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
        return job_sql.to_gql()

    @staticmethod
    def delete_job(db_session: Session, job_id: int) -> bool:
        job_sql = JobRepository.get_job_by_id(
            db_session,
            selected_fields="",
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
        # TODO: Need to adapt SQL get_all to this - filter_by_attr check if list.
        jobs = (
            db_session.query(Job_sql).filter(Job_sql.employer_id.in_(employer_ids))
        ).all()

        return jobs
