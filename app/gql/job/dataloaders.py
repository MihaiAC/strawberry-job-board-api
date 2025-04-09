from strawberry.dataloader import DataLoader
from typing import List
from sqlalchemy.orm import Session
from collections import defaultdict
from app.db.models import Job as Job_sql
from app.db.repositories.job_repository import JobRepository


class JobsFromEmployerDataLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(
        self,
        employer_ids: List[int],
    ) -> List[List[Job_sql]]:
        jobs = JobRepository.get_jobs_by_employer_ids(
            db_session=self.db_session,
            employer_ids=employer_ids,
        )

        grouped = defaultdict(list)
        for job in jobs:
            grouped[job.employer_id].append(job)

        return [grouped[employer_id] for employer_id in employer_ids]
