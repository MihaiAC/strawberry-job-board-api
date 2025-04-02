from starlette.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.data import EMPLOYERS_DATA, JOBS_DATA, APPLICATIONS_DATA, USERS_DATA
from app.db.models import (
    Employer as Employer_sql,
    Job as Job_sql,
    Application as Application_sql,
    User as User_sql,
)
from copy import deepcopy


# TODO: temporary.
from argon2 import PasswordHasher


def post_graphql(
    test_client: TestClient,
    graphql_endpoint: str,
    query: str,
    expected_status: int = 200,
) -> dict:
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == expected_status
    return response.json()


def load_test_tables(session: Session):
    session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
    session.flush()
    session.add_all([Job_sql(**x) for x in JOBS_DATA])
    session.flush()

    users = []
    password_hasher = PasswordHasher()
    for user in USERS_DATA:
        user_copy = deepcopy(user)
        user_copy["password_hash"] = password_hasher.hash(user_copy["password"])
        del user_copy["password"]
        users.append(User_sql(**user_copy))

    session.add_all(users)
    session.flush()

    session.add_all([Application_sql(**x) for x in APPLICATIONS_DATA])
    session.flush()
