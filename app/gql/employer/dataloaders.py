from strawberry.dataloader import DataLoader
from typing import List
from sqlalchemy.orm import Session
from app.db.models import Employer as Employer_sql
from app.db.repositories.employer_repository import EmployerRepository


class EmployerFromJobsDataLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(
        self,
        employer_ids: List[int],
    ) -> List[Employer_sql]:
        employers = EmployerRepository.get_employers_by_ids(
            db_session=self.db_session,
            employer_ids=employer_ids,
        )

        id_to_employer = dict()
        for employer in employers:
            id_to_employer[employer.id] = employer

        return [id_to_employer[employer_id] for employer_id in employer_ids]
