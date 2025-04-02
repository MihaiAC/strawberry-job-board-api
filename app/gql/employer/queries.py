import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.db.models import Employer as Employer_sql, Employer_gql


@strawberry.type
class EmployerQuery:
    @strawberry.field
    def employers(self, info: Info) -> List[Employer_gql]:
        return Employer_sql.fetch_and_transform_to_gql(info)

    @strawberry.field
    def employer(self, id: int, info: Info) -> Optional[Employer_gql]:
        return Employer_sql.fetch_and_transform_to_gql(info, id=id)
