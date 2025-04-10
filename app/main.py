from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager

from .gql.root_mutation import Mutation
from .gql.root_query import Query
from .db.database import prepare_database, get_session
from .db.models import Employer as Employer_sql, Job as Job_sql
from sqlalchemy.orm import Session
from .gql.job.dataloaders import (
    JobsFromEmployerDataLoader,
    JobsFromApplicationDataLoader,
)
from .gql.employer.dataloaders import EmployerFromJobsDataLoader
from .gql.application.dataloaders import (
    AllApplicationsFromJobLoader,
    UserApplicationsFromJobLoader,
    AllApplicationsFromUserLoader,
)
from .gql.user.dataloaders import UsersFromApplicationDataLoader


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


async def get_context(request: Request, db_session: Session = Depends(get_session)):
    return {
        "db_session": db_session,
        "request": request,
        "loaders": {
            "jobs_from_employer": JobsFromEmployerDataLoader(db_session),
            "employer_from_jobs": EmployerFromJobsDataLoader(db_session),
            "user_applications_from_job": UserApplicationsFromJobLoader(db_session),
            "all_applications_from_job": AllApplicationsFromJobLoader(db_session),
            "applications_from_user": AllApplicationsFromUserLoader(db_session),
            "jobs_from_application": JobsFromApplicationDataLoader(db_session),
            "users_from_application": UsersFromApplicationDataLoader(db_session),
        },
    }


schema = Schema(
    query=Query,
    mutation=Mutation,
)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/employers")
def get_employers(session: Session = Depends(get_session)):
    employers = session.query(Employer_sql).all()
    return employers


@app.get("/jobs")
def get_jobs(session: Session = Depends(get_session)):
    jobs = session.query(Job_sql).all()
    return jobs
