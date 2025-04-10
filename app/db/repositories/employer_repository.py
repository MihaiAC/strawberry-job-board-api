from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Employer as Employer_sql
from app.gql.types import Employer_gql
from app.sql_to_gql import employer_to_gql


class EmployerRepository:
    @staticmethod
    def get_all_employers(
        db_session: Session, gql: bool = False
    ) -> List[Employer_gql | Employer_sql]:
        employers = Employer_sql.get_all(db_session=db_session)
        if gql:
            return [employer_to_gql(employer) for employer in employers]
        return employers

    @staticmethod
    def get_employer_by_id(
        db_session: Session,
        id: int,
        gql: bool = False,
    ) -> Optional[Employer_gql | Employer_sql]:
        result = Employer_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"id": id},
        )

        if len(result) == 0:
            return None
        elif gql:
            return employer_to_gql(result[0])
        return result[0]

    @staticmethod
    def get_employer_by_email(
        db_session: Session,
        email: str,
        gql: bool = True,
    ) -> Optional[Employer_gql | Employer_sql]:
        result = Employer_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"contact_email": email},
        )

        if len(result) == 0:
            return None
        elif gql:
            return employer_to_gql(result[0])
        return result[0]

    @staticmethod
    def get_employers_by_ids(
        db_session: Session,
        employer_ids: List[int],
    ) -> List[Employer_sql]:
        return Employer_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"id": employer_ids},
        )
