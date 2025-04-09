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
from app.auth.auth_utils import hash_password, generate_jwt_token
from typing import Tuple, List
from enum import Enum


def post_graphql(
    test_client: TestClient,
    graphql_endpoint: str,
    query: str,
    expected_status: int = 200,
    headers: str = None,
) -> dict:
    response = test_client.post(
        graphql_endpoint, json={"query": query}, headers=headers
    )
    assert response is not None
    assert response.status_code == expected_status
    return response.json()


def load_test_tables(session: Session):
    session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
    session.flush()
    session.add_all([Job_sql(**x) for x in JOBS_DATA])
    session.flush()

    users = []
    for user in USERS_DATA:
        # Deep copy needed since this is run once per test and we don't
        # want to modify the global USERS_DATA.
        user_copy = deepcopy(user)
        user_copy["password_hash"] = hash_password(user_copy["password"])
        del user_copy["password"]
        users.append(User_sql(**user_copy))

    session.add_all(users)
    session.flush()

    session.add_all([Application_sql(**x) for x in APPLICATIONS_DATA])
    session.flush()


def get_test_admin_email() -> str:
    for user in USERS_DATA:
        if user["role"] == "admin":
            return user["email"]
    raise Exception("Test data does not have an admin user.")


def get_test_first_non_admin_user() -> Tuple[int, dict]:
    for idx, user in enumerate(USERS_DATA):
        if user["role"] != "admin":
            return idx, user
    raise Exception("Test data does not have a non-admin user.")


def get_test_first_non_admin_email() -> str:
    _, user = get_test_first_non_admin_user()
    return user["email"]


def get_test_first_non_admin_password() -> str:
    _, user = get_test_first_non_admin_user()
    return user["password"]


def get_test_first_non_admin_id() -> str:
    idx, _ = get_test_first_non_admin_user()
    return idx + 1


def get_job_ids_for_user(user_id: int, applied: bool) -> List[int]:
    job_ids = []
    for application in APPLICATIONS_DATA:
        if application["user_id"] == user_id:
            job_ids.append(application["job_id"])

    if applied:
        return job_ids

    return [job_id for job_id in range(1, len(JOBS_DATA) + 1) if job_id not in job_ids]


def generate_test_jwt_admin_token() -> str:
    for user in USERS_DATA:
        if user["role"] == "admin":
            return generate_jwt_token(user["email"])
    raise Exception("No admin user found in test data.")


def generate_test_jwt_user_token() -> str:
    for user in USERS_DATA:
        if user["role"] == "user":
            return generate_jwt_token(user["email"])
    raise Exception("No admin user found in test data.")


class BaseQueries(str, Enum):
    APPLICATIONS = """query { applications { id } }"""
    CREATE_APPLICATION = """
        mutation {
            applyToJob(jobId: 2)
        }
    """
    LOGIN = f"""mutation {{ loginUser (email: "{get_test_first_non_admin_email()}", password: "{get_test_first_non_admin_password()}")}}"""
    ADD_EMPLOYER = """mutation {
        addEmployer(name: "X", industry: "Y" contactEmail: "ZZZ@AAA.com") {
            id
            name
            industry
            contactEmail
        }
    }
    """
    UPDATE_EMPLOYER = """
    mutation {
        updateEmployer(employerId: 1, name: "updated_name") {
            id
            name
        }
    }
    """
    DELETE_EMPLOYER = """mutation {deleteEmployer(employerId: 1)}"""
    ADD_JOB = """
    mutation {
        addJob(title: "X title", description: "X descr", employerId: 1) {
            id
            title
            description
            employerId
        }
    }
    """
    UPDATE_JOB = """
    mutation {
        updateJob(jobId: 1, title: "new title") {
            id
            title
        }
    }
    """
    DELETE_JOB = """mutation {deleteJob(jobId: 1)}"""
    QUERY_JOB_BY_ID = """query {job(id: 1) {title}}"""
    QUERY_ALL_JOBS = """query {jobs {title}}"""
    QUERY_ALL_USERS = """
    query {
        users {
            id
            email
            username
            role
        }
    }
    """
    ADD_USER = """mutation {
        addUser(
            username: "username",
            email: "email@example.com",
            password: "password",
            role: "user"
        ) {
            id
            username
            email
            role
        }
    }
    """


if __name__ == "__main__":
    print(
        f'Admin test admin header: {{"Authorization": "Bearer {generate_test_jwt_admin_token()}"}} '
    )
    print(
        f'User test admin header: {{"Authorization": "Bearer {generate_test_jwt_user_token()}"}} '
    )
