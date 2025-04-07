from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Job as Job_sql, Job_gql


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
        return Job_sql.get_all(db_session, selected_fields, gql, user_id=user_id)

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
        db_session: Session, selected_fields: str, id: int, gql: bool = True
    ) -> Optional[Job_gql | Job_sql]:
        jobs = Job_sql.get_by_attr(
            db_session,
            selected_fields,
            "id",
            id,
            ignore_fields=["applications"],
            gql=gql,
        )

        return jobs[0] if len(jobs) > 0 else None
