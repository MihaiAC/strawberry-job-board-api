from sqlalchemy.orm import Session
from app.db.models import User as User_sql, User_gql
from typing import Optional, List


class UserRepository:
    # TODO: Update this in a similar way to ApplicationRepository.
    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> Optional[User_sql]:
        return db_session.query(User_sql).filter_by(email=email).first()

    @staticmethod
    def get_all_users(
        db_session: Session, selected_fields: str, gql: bool = True
    ) -> List[User_gql | User_sql]:
        return User_sql.get_all(db_session, selected_fields, gql)

    @staticmethod
    def get_user_by_id(
        db_session: Session, selected_fields: str, id: int, gql: bool = True
    ) -> Optional[User_gql | User_sql]:
        users = User_sql.get_by_attr(db_session, selected_fields, "id", id, gql)
        return users[0] if len(users) > 0 else None
