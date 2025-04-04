from sqlalchemy.orm import Session
from typing import List
from app.db.models import Application as Application_sql, Application_gql


class ApplicationRepository:
    @staticmethod
    def get_all_applications(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[Application_gql | Application_sql]:
        return Application_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_all_applications_by_user_id(
        db_session: Session, selected_fields: str, user_id: int, gql: bool = True
    ) -> List[Application_gql | Application_sql]:
        return Application_sql.get_by_attr(
            db_session, selected_fields, "user_id", user_id, gql
        )

    @staticmethod
    def get_all_applications_by_job_id(
        db_session: Session, selected_fields: str, job_id: int, gql: bool = True
    ) -> List[Application_gql | Application_sql]:
        return Application_sql.get_by_attr(
            db_session, selected_fields, "job_id", job_id, gql
        )
