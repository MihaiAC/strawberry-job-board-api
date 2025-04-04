import strawberry
from strawberry.types import Info
from app.db.models import User as User_sql, User_gql
from graphql import GraphQLError
from app.auth_utils import (
    verify_password,
    generate_jwt_token,
    hash_password,
)
from app.db.repositories.user_repository import UserRepository


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    def login_user(email: str, password: str, info: Info) -> str:
        # TODO: Should use .get and handle errors explicitly.
        db_session = info.context["db_session"]
        # request = info.context["request"]

        user_sql = UserRepository.get_user_by_email(db_session, email)

        if not user_sql:
            raise GraphQLError("User does not exist")

        verify_password(user_sql.password_hash, password)
        token = generate_jwt_token(email)
        return token


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def add_user(
        username: str, email: str, password: str, role: str, info: Info
    ) -> User_gql:
        db_session = info.context["db_session"]

        # Only an admin can add another admin.
        if role == "admin":
            request = info.context["request"]
            authenticated_user = UserRepository.get_authenticated_user(
                db_session, request
            )

            if authenticated_user.role != "admin":
                raise GraphQLError("Only admin users can add new admin users.")

        user = UserRepository.get_user_by_email(db_session, email)

        if user:
            raise GraphQLError("A user with that email already exists.")

        password_hash = hash_password(password)
        user = User_sql(
            username=username, email=email, password_hash=password_hash, role=role
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user.to_gql()
