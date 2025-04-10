from sqlalchemy.orm import Session
from typing import List, Tuple
from app.db.models import Application as Application_sql
from app.gql.types import Application_gql
from graphql import GraphQLError
from app.errors.error_messages import ALREADY_APPLIED
from app.errors.custom_errors import ResourceNotFound
from .job_repository import JobRepository
from app.sql_to_gql import application_to_gql


class ApplicationRepository:
    @staticmethod
    def get_all_applications(
        db_session: Session, gql: bool = False
    ) -> List[Application_gql | Application_sql]:
        applications = Application_sql.get_all(db_session)
        if gql:
            return [application_to_gql(app) for app in applications]
        return applications

    @staticmethod
    def get_all_applications_by_user_id(
        db_session: Session, user_id: int, gql: bool = False
    ) -> List[Application_gql | Application_sql]:
        applications = Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"user_id": user_id},
        )

        if gql:
            return [application_to_gql(app) for app in applications]
        return applications

    @staticmethod
    def get_all_applications_by_job_id(
        db_session: Session, job_id: int, gql: bool = False
    ) -> List[Application_gql | Application_sql]:
        applications = Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"job_id": job_id},
        )

        if gql:
            return [application_to_gql(app) for app in applications]
        return applications

    @staticmethod
    def get_applications_from_job_ids(
        db_session: Session,
        job_ids: List[int],
    ) -> List[Application_sql]:
        return Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"job_id": job_ids},
        )

    @staticmethod
    def get_applications_from_user_ids(
        db_session: Session,
        user_ids: List[int],
    ) -> List[Application_sql]:
        return Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"user_id": user_ids},
        )

    @staticmethod
    def get_all_applications_from_job_user_ids(
        db_session: Session,
        job_user_id_tuples: List[Tuple[int, int]],
    ) -> List[Application_sql]:
        return Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={("job_id", "user_id"): job_user_id_tuples},
        )

    @staticmethod
    def create_application(db_session: Session, user_id: int, job_id: int) -> bool:
        job = JobRepository.get_job_by_id(
            db_session=db_session,
            id=job_id,
            gql=False,
        )

        if job is None:
            raise ResourceNotFound("Job")

        user_applications = Application_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"user_id": user_id, "job_id": job_id},
        )

        for application in user_applications:
            if application.job_id == job_id:
                raise GraphQLError(ALREADY_APPLIED)

        application_sql = Application_sql(user_id=user_id, job_id=job_id)
        db_session.add(application_sql)
        db_session.commit()

        return True
