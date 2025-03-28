import strawberry
from typing import List
from .types import (
    Job as Job_gql,
    Employer as Employer_gql,
    JOBS,
    EMPLOYERS,
)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str) -> str:
        return f"Hello {name}"

    @strawberry.field
    def jobs(self) -> List[Job_gql]:
        return JOBS

    @strawberry.field
    def employers(self) -> List[Employer_gql]:
        return list(EMPLOYERS.values())
