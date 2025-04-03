import strawberry
from strawberry.types import Info
from app.db.models import User as User_sql
from graphql import GraphQLError
from app.auth_utils import (
    verify_password,
    generate_jwt_token,
)


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    def login_user(email: str, password: str, info: Info) -> str:
        # TODO: Should use .get and handle errors explicitly.
        db_session = info.context["db_session"]
        # request = info.context["request"]

        user_sql = User_sql.get_user_by_email(db_session, email)

        if not user_sql:
            raise GraphQLError("User does not exist")

        verify_password(user_sql.password_hash, password)
        token = generate_jwt_token(email)
        return token
