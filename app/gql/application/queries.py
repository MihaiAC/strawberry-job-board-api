import strawberry
from typing import List
from strawberry.types import Info
from app.db.models import Application as Application_sql, Application_gql


@strawberry.type
class ApplicationQuery:
    @strawberry.field
    def applications(self, info: Info) -> List[Application_gql]:
        db_session = info.context["db_session"]
        applications = db_session.query(Application_sql).all()
        return applications
