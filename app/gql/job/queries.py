import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.db.models import Job as Job_sql, Job_gql


@strawberry.type
class JobQuery:
    # Given a job, allow retrieval of all other jobs from this employer.
    @strawberry.field
    def jobs(self, info: Info) -> List[Job_gql]:
        return Job_sql.fetch_and_transform_to_gql(info)

    @strawberry.field
    def job(self, id: int, info: Info) -> Optional[Job_gql]:
        return Job_sql.fetch_and_transform_to_gql(info, id=id)
