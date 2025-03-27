import strawberry

from typing import List
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI
from contextlib import asynccontextmanager

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# Beginning part = "dialect".
DATABASE_URL = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create engine.
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class EmployerObject(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    contact_email: Mapped[str] = mapped_column(String(254))
    industry: Mapped[str] = mapped_column(String(254))
    jobs: Mapped[List["JobObject"]] = relationship(
        back_populates="employer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Employer(id={self.id!r}, name={self.name!r}, "
            f"contact_email={self.contact_email!r}, "
            f"industry={self.industry!r})"
        )


class JobObject(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))
    employer: Mapped["EmployerObject"] = relationship(
        "EmployerObject",
        back_populates="jobs",
    )


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


# Drop tables on rerun.
def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([EmployerObject(**x) for x in employers_data])
        session.add_all([JobObject(**x) for x in jobs_data])
        session.commit()


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
