import strawberry
from typing import List
from strawberry.types import Info
from app.gql.types import User as User_gql
from app.db.models import User as User_sql


@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self, info: Info) -> List[User_gql]:
        db_session = info.context["db_session"]
        users = db_session.query(User_sql).all()
        return users
