import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.gql.types import Employer_gql
from app.db.repositories.employer_repository import EmployerRepository


@strawberry.type
class EmployerQuery:
    @strawberry.field
    def employers(self, info: Info) -> List[Employer_gql]:
        db_session = info.context["db_session"]
        return EmployerRepository.get_all_employers(db_session, gql=True)

    @strawberry.field
    def employer(self, id: int, info: Info) -> Optional[Employer_gql]:
        db_session = info.context["db_session"]
        return EmployerRepository.get_employer_by_id(
            db_session,
            id,
            gql=True,
        )
