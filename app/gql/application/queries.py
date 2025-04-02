import strawberry
from typing import List
from strawberry.types import Info
from app.db.models import Application as Application_sql, Application_gql


@strawberry.type
class ApplicationQuery:
    @strawberry.field
    def applications(self, info: Info) -> List[Application_gql]:
        return Application_sql.fetch_and_transform_to_gql(info)
