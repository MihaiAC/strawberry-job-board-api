from strawberry.dataloader import DataLoader
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.db.models import Application as Application_sql
from app.db.repositories.application_repository import ApplicationRepository
from collections import defaultdict


class UserApplicationsFromJobLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(
        self,
        job_user_id_tuples: List[Tuple[int, int]],
    ) -> List[Application_sql]:

        applications = ApplicationRepository.get_all_applications_from_job_user_ids(
            self.db_session,
            job_user_id_tuples,
        )

        # Return in correct order.
        app_dict = {(app.job_id, app.user_id): app for app in applications}
        return [
            app_dict.get((job_id, user_id)) for job_id, user_id in job_user_id_tuples
        ]


class AllApplicationsFromJobLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(self, job_ids: List[int]) -> List[List[Application_sql]]:
        applications = ApplicationRepository.get_applications_from_job_ids(
            self.db_session,
            job_ids,
        )

        # Return in correct order.
        job_id_to_applications = defaultdict(list)
        for application in applications:
            job_id_to_applications[application.job_id].append(application)

        return [job_id_to_applications[job_id] for job_id in job_ids]


class AllApplicationsFromUserLoader(DataLoader):
    def __init__(self, db_session: Session):
        super().__init__(load_fn=self.batch_load_fn)
        self.db_session = db_session

    async def batch_load_fn(self, user_ids: List[int]) -> List[List[Application_sql]]:
        applications = ApplicationRepository.get_applications_from_user_ids(
            self.db_session, user_ids
        )

        # Return in correct order.
        user_id_to_applications = defaultdict(list)
        for application in applications:
            user_id_to_applications[application.user_id].append(application)

        return [user_id_to_applications[user_id] for user_id in user_ids]
