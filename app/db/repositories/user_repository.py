from sqlalchemy.orm import Session
from app.db.models import User as User_sql
from typing import Optional
from fastapi import Request
from app.auth_utils import get_user_email_from_request_token
from graphql import GraphQLError


class UserRepository:
    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> Optional[User_sql]:
        return db_session.query(User_sql).filter_by(email=email).first()

    @staticmethod
    def get_authenticated_user(db_session: Session, request: Request) -> User_sql:
        request_user_email = get_user_email_from_request_token(request)
        request_user = UserRepository.get_user_by_email(
            db_session,
            request_user_email,
        )

        if request_user is None:
            raise GraphQLError("Authenticated user not found.")

        return request_user
