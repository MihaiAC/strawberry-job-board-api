from sqlalchemy.orm import Session
from typing import List
from app.db.models import Job as Job_sql, Job_gql


class JobRepository:
    @staticmethod
    def get_all_jobs(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[Job_gql | Job_sql]:
        return Job_sql.get_all(db_session, selected_fields, gql)

    # @staticmethod
    # def get_all_jobs_by_id(
    #     db_session: Session, selected_fields: str, id: int, gql: bool = True
    # ) -> List[Job_gql | Job_sql]:
    #     return Job_sql.get_by_attr(db_session, selected_fields, "id", id, gql)

    @staticmethod
    def get_all_jobs_by_employer_id(
        db_session: Session, selected_fields: str, employer_id: int, gql: bool = True
    ) -> List[Job_gql | Job_sql]:
        return Job_sql.get_by_attr(
            db_session, selected_fields, "employer_id", employer_id, gql
        )
