import strawberry
from typing import List
from app.db.data import EMPLOYERS_DATA, JOBS_DATA


# Way to handle circular references.
@strawberry.type
class Employer:
    id: int
    name: str
    contact_email: str
    industry: str
    jobs: List["Job"]


@strawberry.type
class Job:
    id: int
    title: str
    description: str
    employer_id: int
    employer: Employer


# This should be handled by the ORM normally, curious if this works.
# It did work!
EMPLOYERS = {e["id"]: Employer(**e, jobs=[]) for e in EMPLOYERS_DATA}
JOBS = [Job(**job, employer=EMPLOYERS[job["employer_id"]]) for job in JOBS_DATA]

for job in JOBS:
    job.employer.jobs.append(job)
