from sqlalchemy.orm import Session
from typing import List
from app.db.models import Application as Application_sql, Application_gql
from graphql import GraphQLError
from app.errors.error_messages import ALREADY_APPLIED
from app.errors.custom_errors import ResourceNotFound
from .job_repository import JobRepository


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

    # TODO: After merging get functions, add attr list to args + retrieve
    # application by both user_id and job_id to check if it already exists.
    @staticmethod
    def create_application(db_session: Session, user_id: int, job_id: int) -> bool:
        user_applications = ApplicationRepository.get_all_applications_by_user_id(
            db_session=db_session, selected_fields="", user_id=user_id, gql=False
        )

        job = JobRepository.get_job_by_id(
            db_session=db_session,
            selected_fields="",
            id=job_id,
        )

        if job is None:
            raise ResourceNotFound("Job")

        for application in user_applications:
            if application.job_id == job_id:
                raise GraphQLError(ALREADY_APPLIED)

        application_sql = Application_sql(user_id=user_id, job_id=job_id)
        db_session.add(application_sql)
        db_session.commit()

        return True
