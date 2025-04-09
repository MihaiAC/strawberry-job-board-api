from sqlalchemy.orm import Session
from app.db.models import User as User_sql
from typing import Optional, List


class UserRepository:
    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> Optional[User_sql]:
        user = User_sql.get_all(
            db_session=db_session,
            selected_fields="",
            filter_by_attrs={"email": email},
            gql=False,
        )
        return user[0] if len(user) > 0 else None

    @staticmethod
    def get_all_users(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[User_sql]:
        return User_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_user_by_id(
        db_session: Session, selected_fields: str, id: int, gql: bool = True
    ) -> Optional[User_sql]:
        users = User_sql.get_all(
            db_session=db_session,
            selected_fields=selected_fields,
            filter_by_attrs={"id": id},
            gql=gql,
        )
        return users[0] if len(users) > 0 else None
