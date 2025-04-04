from sqlalchemy.orm import Session
from app.db.models import User as User_sql
from typing import Optional


class UserRepository:
    # TODO: Update this in a similar way to ApplicationRepository.
    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> Optional[User_sql]:
        return db_session.query(User_sql).filter_by(email=email).first()
