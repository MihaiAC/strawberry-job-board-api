from strawberry.dataloader import DataLoader
from typing import List
from sqlalchemy.orm import Session
from app.db.models import User as User_sql
from app.db.repositories.user_repository import UserRepository


class UsersFromApplicationDataLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(self, user_ids: List[int]) -> List[User_sql]:
        users = UserRepository.get_users_by_ids(self.db_session, user_ids)

        user_ids_to_user = dict()
        for user in users:
            user_ids_to_user[user.id] = user

        return [user_ids_to_user.get(user_id, None) for user_id in user_ids]
