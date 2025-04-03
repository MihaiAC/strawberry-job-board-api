import strawberry
from strawberry.types import Info
from app.db.models import User as User_sql
from graphql import GraphQLError
from app.auth_utils import generate_jwt_token, verify_password


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    def login_user(email: str, password: str, info: Info) -> str:
        db_session = info.context["db_session"]
        user_sql = db_session.query(User_sql).filter(User_sql.email == email).first()

        if not user_sql:
            raise GraphQLError("User does not exist")

        verify_password(user_sql.password_hash, password)
        token = generate_jwt_token(email)
        return token
