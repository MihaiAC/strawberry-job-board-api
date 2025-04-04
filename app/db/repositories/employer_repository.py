from sqlalchemy.orm import Session
from typing import List
from app.db.models import Employer as Employer_sql, Employer_gql


class EmployerRepository:
    # @staticmethod
    # def get_all_employers(
    #     db_session: Session, selected_fields: str, gql: bool = True
    # ) -> List[Employer_gql | Employer_sql]:
    #     return Employer_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_all_employers_by_id(
        db_session: Session, selected_fields: str, id: int, gql: bool = True
    ) -> List[Employer_gql | Employer_sql]:
        return Employer_sql.get_by_attr(db_session, selected_fields, "id", id, gql)
