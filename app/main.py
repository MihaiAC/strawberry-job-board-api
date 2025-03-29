from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from .gql.queries import Query
from .gql.mutations import Mutation
from .db.database import prepare_database, get_session
from .db.models import Employer as Employer_sql, Job as Job_sql
from sqlalchemy.orm import Session


schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


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
