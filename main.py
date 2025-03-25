import strawberry

from typing import List
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

employers_data = [
    {
        "id": 1,
        "name": "MetaTechA",
        "contact_email": "contact@company-a.com",
        "industry": "Tech",
    },
    {
        "id": 2,
        "name": "MoneySoftB",
        "contact_email": "contact@company-b.com",
        "industry": "Finance",
    },
]

jobs_data = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Develop web applications",
        "employer_id": 1,
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "description": "Analyze data and create reports",
        "employer_id": 1,
    },
    {
        "id": 3,
        "title": "Accountant",
        "description": "Manage financial records",
        "employer_id": 2,
    },
    {
        "id": 4,
        "title": "Manager",
        "description": "Manage people who manage records",
        "employer_id": 2,
    },
]


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
employers = {e["id"]: Employer(**e, jobs=[]) for e in employers_data}
jobs = [Job(**job, employer=employers[job["employer_id"]]) for job in jobs_data]

for job in jobs:
    job.employer.jobs.append(job)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str) -> str:
        return f"Hello {name}"

    @strawberry.field
    def jobs(self) -> List[Job]:
        return jobs

    @strawberry.field
    def employers(self) -> List[Employer]:
        return list(employers.values())


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
