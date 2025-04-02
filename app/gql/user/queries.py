import strawberry
from typing import List
from strawberry.types import Info
from app.db.models import User as User_sql, User_gql


@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self, info: Info) -> List[User_gql]:
        db_session = info.context["db_session"]
        users = db_session.query(User_sql).all()
        return users
