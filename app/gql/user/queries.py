import strawberry
from typing import List
from strawberry.types import Info
from app.db.models import User as User_sql, User_gql


@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self, info: Info) -> List[User_gql]:
        return User_sql.fetch_and_transform_to_gql(info)
