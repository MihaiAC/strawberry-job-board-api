from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from fastapi import FastAPI
from contextlib import asynccontextmanager

from .gql.queries import Query
from .db.database import prepare_database


schema = Schema(Query)
graphql_app = GraphQLRouter(schema)


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
