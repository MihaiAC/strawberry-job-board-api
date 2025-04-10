import pytest
from app.db.data import JOBS_DATA, EMPLOYERS_DATA, USERS_DATA, APPLICATIONS_DATA
from .utils import (
    post_graphql,
    get_test_first_non_admin_id,
    get_test_first_non_admin_email,
    get_job_ids_for_user,
    get_application_ids_for_job,
    get_application_ids_for_user,
)
from collections import defaultdict


@pytest.mark.api
@pytest.mark.query
def test_get_all_jobs(test_client, graphql_endpoint):
    query = """
        query {
            jobs {
                title
            }
        }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    jobs = result["data"]["jobs"]
    assert len(jobs) == len(JOBS_DATA)
    assert sorted([job["title"] for job in jobs]) == sorted(
        job["title"] for job in JOBS_DATA
    )


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_job_by_id_all_roles(
    test_client, graphql_endpoint, admin_header, user_header
):
    user_job_ids = get_job_ids_for_user(2, applied=True)
    for job_id in range(1, len(JOBS_DATA) + 1):
        query = f"""
        query {{
            job(id: {job_id}) {{
                id
                employerId
                title
                employer {{
                    name
                }}
                applications {{
                    id
                    jobId
                    userId
                }}
            }}
        }}
        """
        # Unauth.
        result = post_graphql(test_client, graphql_endpoint, query, headers="")
        job = result["data"]["job"]
        assert job["title"] == JOBS_DATA[job_id - 1]["title"]
        assert job["applications"] == []
        assert EMPLOYERS_DATA[job["employerId"] - 1]["name"] == job["employer"]["name"]

        # User.
        result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
        job = result["data"]["job"]
        assert job["title"] == JOBS_DATA[job_id - 1]["title"]
        if job_id in user_job_ids:
            assert len(job["applications"]) == 1
            assert job["applications"][0]["userId"] == 2
            assert job["applications"][0]["jobId"] == job_id
        else:
            assert len(job["applications"]) == 0

        # Admin.
        result = post_graphql(
            test_client, graphql_endpoint, query, headers=admin_header
        )
        job = result["data"]["job"]
        assert job["title"] == JOBS_DATA[job_id - 1]["title"]

        application_ids = get_application_ids_for_job(job_id)
        assert len(job["applications"]) == len(application_ids)
        retrieved_app_ids = [x["id"] for x in job["applications"]]
        assert sorted(application_ids) == sorted(
            retrieved_app_ids
        ), f"Job_id: {job_id} expected {sorted(application_ids)}, got {sorted(retrieved_app_ids)}"


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_all_jobs_admin(test_client, graphql_endpoint, admin_header):
    """Tests admin can get all the jobs and respective applications."""
    query = """
        query {
            jobs {
                id
                title
                employer {
                    name
                }
                applications {
                    jobId
                    userId
                }
            }
        }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    jobs = result["data"]["jobs"]
    assert len(jobs) == len(JOBS_DATA)

    unique_apps = set()
    for job in jobs:
        for application in job["applications"]:
            assert {
                "user_id": application["userId"],
                "job_id": application["jobId"],
            } in APPLICATIONS_DATA
            unique_apps.add((application["userId"], application["jobId"]))

    assert len(unique_apps) == len(APPLICATIONS_DATA)


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_all_jobs_user(test_client, graphql_endpoint, user_header):
    """Tests user only gets his applications."""
    query = """
        query {
            jobs {
                id
                title
                employer {
                    name
                }
                applications {
                    jobId
                    userId
                }
            }
        }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    jobs = result["data"]["jobs"]
    assert len(jobs) == len(JOBS_DATA)

    for job in jobs:
        if len(job["applications"]) > 0:
            for application in job["applications"]:
                assert application["userId"] == get_test_first_non_admin_id()


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_all_jobs_unauth(test_client, graphql_endpoint):
    """Tests user only gets his applications."""
    query = """
        query {
            jobs {
                id
                title
                employer {
                    name
                }
                applications {
                    jobId
                    userId
                }
            }
        }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    jobs = result["data"]["jobs"]
    assert len(jobs) == len(JOBS_DATA)

    for job in jobs:
        assert job["applications"] is None or len(job["applications"]) == 0


@pytest.mark.api
@pytest.mark.query
def test_get_all_employers(test_client, graphql_endpoint):
    query = """
    query {
        employers {
            name
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employers = result["data"]["employers"]
    assert len(employers) == len(EMPLOYERS_DATA)
    assert sorted([employer["name"] for employer in employers]) == sorted(
        employer["name"] for employer in EMPLOYERS_DATA
    )


@pytest.mark.api
@pytest.mark.query
def test_get_employer_by_id(test_client, graphql_endpoint):
    for employer_idx in range(len(EMPLOYERS_DATA)):
        query = f"""
        query {{
            employer(id: {employer_idx+1}) {{
                name
            }}
        }}
        """
        result = post_graphql(test_client, graphql_endpoint, query)
        employer = result["data"]["employer"]
        assert employer["name"] == EMPLOYERS_DATA[employer_idx]["name"]


# This is playing a bit fast and loose with the IDs.
@pytest.mark.api
@pytest.mark.query
def test_get_employer_from_job(test_client, graphql_endpoint):
    query = """
    query {
        job(id: 1) {
            title
            employer {
            name
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["job"]
    assert job["title"] == JOBS_DATA[0]["title"]
    assert job["employer"]["name"] == EMPLOYERS_DATA[0]["name"]


@pytest.mark.api
@pytest.mark.query
def test_get_jobs_from_employer(test_client, graphql_endpoint):
    query = """
    query {
        employer(id: 1) {
            name
            jobs {
            title
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employer = result["data"]["employer"]
    assert employer["name"] == EMPLOYERS_DATA[0]["name"]
    assert len(employer["jobs"]) == 2
    assert sorted([job["title"] for job in employer["jobs"]]) == sorted(
        [job["title"] for job in JOBS_DATA[:2]]
    )


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_all_users_as_admin(test_client, graphql_endpoint, admin_header):
    query = """
    query {
        users {
            id
            email
            username
            role
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    users = result["data"]["users"]
    assert len(users) == len(USERS_DATA)
    assert sorted([user["username"] for user in users]) == sorted(
        user["username"] for user in USERS_DATA
    )


@pytest.mark.api
@pytest.mark.query
@pytest.mark.auth
def test_get_all_users_as_user(test_client, graphql_endpoint, user_header):
    query = """
    query {
        users {
            id
            email
            username
            role
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    users = result["data"]["users"]
    assert len(users) == 1
    assert users[0]["id"] == get_test_first_non_admin_id()
    assert users[0]["email"] == get_test_first_non_admin_email()


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications_as_admin(test_client, graphql_endpoint, admin_header):
    query = """
    query {
        applications {
            jobId
            job {
                id
                title
            }
            userId
            user {
                id
                username
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    applications = result["data"]["applications"]
    assert len(applications) == len(APPLICATIONS_DATA)

    # Testing correct relationship retrieval.
    for application in applications:
        assert application["jobId"] == application["job"]["id"]
        assert application["userId"] == application["user"]["id"]

    user_id_to_username = defaultdict(str)
    for idx, user in enumerate(USERS_DATA):
        user_id_to_username[idx + 1] = user["username"]

    job_id_to_title = defaultdict(str)
    for idx, job in enumerate(JOBS_DATA):
        job_id_to_title[idx + 1] = job["title"]

    for idx in range(len(applications)):
        job_title = applications[idx]["job"]["title"]
        job_id = applications[idx]["jobId"]
        assert job_title == job_id_to_title[job_id]

        username = applications[idx]["user"]["username"]
        user_id = applications[idx]["userId"]
        assert username == user_id_to_username[user_id]


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications_as_user(test_client, graphql_endpoint, user_header):
    query = """
    query {
        applications {
            jobId
            job {
                id
                title
            }
            userId
            user {
                id
                username
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    applications = result["data"]["applications"]

    # Get the authenticated user's ID.
    auth_user_id = get_test_first_non_admin_id()

    # Test we are retrieving only the applications of the current user.
    application_count = 0
    for application in APPLICATIONS_DATA:
        if application["user_id"] == auth_user_id:
            application_count += 1

    assert len(applications) == application_count
    for application in applications:
        assert application["user"]["id"] == application["userId"] == auth_user_id


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications_for_user(test_client, graphql_endpoint, user_header):
    query = """
    query {
        users {
            id
            username
            email
            applications {
                id
                userId
                jobId
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)

    users = result["data"]["users"]
    assert len(users) == 1

    user_id = get_test_first_non_admin_id()
    user = users[0]
    assert user["id"] == user_id

    applications = user["applications"]
    retrieved_app_ids = [app["id"] for app in applications]
    expected_app_ids = get_application_ids_for_user(user_id)

    assert sorted(retrieved_app_ids) == sorted(
        expected_app_ids
    ), f"{retrieved_app_ids} {expected_app_ids}"


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications_for_admin(test_client, graphql_endpoint, admin_header):
    query = """
    query {
        users {
            id
            username
            email
            applications {
                id
                userId
                jobId
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)

    users = result["data"]["users"]
    assert len(users) == len(USERS_DATA)

    for user_id in range(1, len(users) + 1):
        found = False
        for user in users:
            if user["id"] == user_id:
                found = True
                break

        assert found, f"User with id {user_id} not found."

        applications = user["applications"]
        retrieved_app_ids = [app["id"] for app in applications]
        expected_app_ids = get_application_ids_for_user(user_id)

        assert sorted(retrieved_app_ids) == sorted(
            expected_app_ids
        ), f"{retrieved_app_ids} {expected_app_ids}"
