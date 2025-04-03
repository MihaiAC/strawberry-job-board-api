from strawberry import Schema
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import QueryDepthLimiter

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager

from .gql.root_mutation import Mutation
from .gql.root_query import Query
from .db.database import prepare_database, get_session
from .db.models import Employer as Employer_sql, Job as Job_sql
from sqlalchemy.orm import Session


# TODO: How can you limit a query's lateral depth?
# TODO: How can you limit the number of records returned?
# TODO: How can you limit the number of queries a user can perform in a
# given time window?
# TODO: Should use strawberry input types.
@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


async def get_context(request: Request, db_session: Session = Depends(get_session)):
    return {
        "db_session": db_session,
        "request": request,
    }


schema = Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(
            max_depth=2,
        )
    ],
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
