import strawberry
import string
from random import choices
from strawberry.types import Info
from app.db.models import User as User_sql
from graphql import GraphQLError

# TODO: temporary, change
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    def login_user(email: str, password: str, info: Info) -> str:
        db_session = info.context["db_session"]
        user_sql = db_session.query(User_sql).filter(User_sql.email == email).first()

        # TODO: or password is wrong
        if not user_sql:
            raise GraphQLError("User does not exist")

        try:
            hasher = PasswordHasher()
            hasher.verify(user_sql.password_hash, password)
        except VerifyMismatchError:
            raise GraphQLError("Invalid password")

        token = "".join(choices(string.ascii_lowercase, k=10))

        return token
