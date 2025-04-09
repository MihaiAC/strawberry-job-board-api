import strawberry
from strawberry.types import Info
from app.db.models import User as User_sql
from app.gql.types import User_gql
from graphql import GraphQLError
from app.auth.auth_utils import (
    verify_password,
    generate_jwt_token,
    hash_password,
    require_role,
)
from app.db.repositories.user_repository import UserRepository
from app.errors.custom_errors import ResourceNotFound
from app.errors.error_messages import (
    USER_ALREADY_EXISTS,
    INSUFFICIENT_PRIVILEGES,
    INVALID_ROLE,
)
from app.auth.roles import Role


@strawberry.type
class LoginMutation:
    @strawberry.mutation
    @require_role([Role.UNAUTHENTICATED])
    def login_user(email: str, password: str, info: Info) -> str:
        db_session = info.context["db_session"]

        user_sql = UserRepository.get_user_by_email(db_session, email)

        if not user_sql:
            raise ResourceNotFound("User")

        verify_password(user_sql.password_hash, password)
        token = generate_jwt_token(email)
        return token


@strawberry.type
class UserMutation:

    @strawberry.mutation
    @require_role([Role.ADMIN, Role.UNAUTHENTICATED])
    def add_user(
        username: str, email: str, password: str, role: str, info: Info
    ) -> User_gql:
        db_session = info.context["db_session"]

        # Only an admin can add another admin.
        if role == Role.ADMIN:
            if info.context["user"] is None or info.context["user"].role != Role.ADMIN:
                raise GraphQLError(INSUFFICIENT_PRIVILEGES)

        if role == Role.USER or role == Role.ADMIN:
            user_to_add = UserRepository.get_user_by_email(db_session, email)

            if user_to_add is not None:
                raise GraphQLError(USER_ALREADY_EXISTS)

            password_hash = hash_password(password)
            user_to_add = User_sql(
                username=username, email=email, password_hash=password_hash, role=role
            )
            db_session.add(user_to_add)
            db_session.commit()
            db_session.refresh(user_to_add)

            return user_to_add.to_gql()
        else:
            raise GraphQLError(INVALID_ROLE)
