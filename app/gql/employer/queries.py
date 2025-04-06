import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.db.models import Employer_gql
from app.db.repositories.employer_repository import EmployerRepository


@strawberry.type
class EmployerQuery:
    @strawberry.field
    def employers(self, info: Info) -> List[Employer_gql]:
        db_session = info.context["db_session"]
        selected_fields = str(info.selected_fields)

        return EmployerRepository.get_all_employers(
            db_session, selected_fields, gql=True
        )

    @strawberry.field
    def employer(self, id: int, info: Info) -> Optional[Employer_gql]:
        db_session = info.context["db_session"]
        selected_fields = str(info.selected_fields)

        return EmployerRepository.get_employer_by_id(
            db_session, selected_fields, id, gql=True
        )
