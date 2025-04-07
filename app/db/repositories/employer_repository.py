from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Employer as Employer_sql, Employer_gql


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
        result = Employer_sql.get_by_attr(db_session, selected_fields, "id", id, gql)
        return None if len(result) == 0 else result[0]

    @staticmethod
    def get_employer_by_email(
        db_session: Session,
        selected_fields: str,
        email: str,
        gql: bool = True,
    ) -> Optional[Employer_gql | Employer_sql]:
        result = Employer_sql.get_by_attr(
            db_session=db_session,
            selected_fields=selected_fields,
            attr_name="contact_email",
            attr_value=email,
            gql=gql,
        )
        return None if len(result) == 0 else result[0]
