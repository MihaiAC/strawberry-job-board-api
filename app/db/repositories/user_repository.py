from sqlalchemy.orm import Session
from app.db.models import User as User_sql
from typing import Optional, List
from app.sql_to_gql import user_to_gql


class UserRepository:
    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> Optional[User_sql]:
        user = User_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"email": email},
        )
        return user[0] if len(user) > 0 else None

    @staticmethod
    def get_all_users(db_session: Session, gql: bool = True) -> List[User_sql]:
        users = User_sql.get_all(db_session)
        if gql:
            return list(map(user_to_gql, users))
        return users

    @staticmethod
    def get_user_by_id(
        db_session: Session, id: int, gql: bool = True
    ) -> Optional[User_sql]:
        users = User_sql.get_all(
            db_session=db_session,
            filter_by_attrs={"id": id},
        )

        if len(users) == 0:
            return None
        elif gql:
            return user_to_gql(users[0])
        return users[0]
