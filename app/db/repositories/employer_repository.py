from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Employer as Employer_sql
from app.gql.types import Employer_gql


class EmployerRepository:
    @staticmethod
    def get_all_employers(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[Employer_gql | Employer_sql]:
        return Employer_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_employer_by_id(
        db_session: Session,
        selected_fields: str,
        id: int,
        gql: bool = True,
    ) -> Optional[Employer_gql | Employer_sql]:
        result = Employer_sql.get_all(
            db_session=db_session,
            selected_fields=selected_fields,
            filter_by_attrs={"id": id},
            gql=gql,
        )
        return None if len(result) == 0 else result[0]

    @staticmethod
    def get_employer_by_email(
        db_session: Session,
        selected_fields: str,
        email: str,
        gql: bool = True,
    ) -> Optional[Employer_gql | Employer_sql]:
        result = Employer_sql.get_all(
            db_session=db_session,
            selected_fields=selected_fields,
            filter_by_attrs={"contact_email": email},
            gql=gql,
        )
        return None if len(result) == 0 else result[0]

    @staticmethod
    def get_employers_by_ids(
        db_session: Session,
        employer_ids: List[int],
    ) -> List[Employer_sql]:
        employers = (
            db_session.query(Employer_sql).filter(Employer_sql.id.in_(employer_ids))
        ).all()

        return employers
