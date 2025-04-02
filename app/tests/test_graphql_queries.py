import pytest
from app.db.data import JOBS_DATA, EMPLOYERS_DATA, USERS_DATA, APPLICATIONS_DATA
from .test_utils import post_graphql
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
def test_get_job_by_id(test_client, graphql_endpoint):
    query = """
        query {
        job(id: 1) {
            title
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["job"]
    assert job["title"] == JOBS_DATA[0]["title"]


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
    query = """
    query {
        employer(id: 1) {
            name
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employer = result["data"]["employer"]
    assert employer["name"] == EMPLOYERS_DATA[0]["name"]


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
def test_circular_reference_depth_limit(test_client, graphql_endpoint):
    # Should not pass.
    query = """
    query {
        employers {
            jobs {
            employer {
                name
            }
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"] is None
    assert len(result["errors"]) >= 1

    # Should pass.
    query = """
    query {
        job(id: 1) {
            employer {
                name
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["job"]
    assert job["employer"]["name"] == EMPLOYERS_DATA[0]["name"]


@pytest.mark.api
@pytest.mark.query
def test_get_all_users(test_client, graphql_endpoint):
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
    result = post_graphql(test_client, graphql_endpoint, query)
    users = result["data"]["users"]
    assert len(users) == len(USERS_DATA)
    assert sorted([user["username"] for user in users]) == sorted(
        user["username"] for user in USERS_DATA
    )
    # TODO: Still needed?
    for user in users:
        assert "password" not in user


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications(test_client, graphql_endpoint):
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
    result = post_graphql(test_client, graphql_endpoint, query)
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
