import pytest
from app.db.data import JOBS_DATA, EMPLOYERS_DATA, USERS_DATA, APPLICATIONS_DATA


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

    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    employer = result["data"]["employer"]
    assert employer["name"] == EMPLOYERS_DATA[0]["name"]
    assert len(employer["jobs"]) == 2
    assert sorted([job["title"] for job in employer["jobs"]]) == sorted(
        [job["title"] for job in JOBS_DATA[:2]]
    )


# TODO: Need to rewrite this after applying depth limiter plugin.
# @pytest.mark.api
# @pytest.mark.query
# def test_circular_reference_depth_limit(test_client, graphql_endpoint):
#     # Should not pass.
#     query = """
#     query {
#         employers {
#             jobs {
#             employer {
#                 name
#             }
#             }
#         }
#     }
#     """
#     response = test_client.post(graphql_endpoint, json={"query": query})
#     assert response is not None
#     assert response.status_code == 200

#     result = response.json()
#     assert result["data"] is None
#     assert len(result["errors"]) >= 1

#     # Should pass.
#     query = """
#     query {
#         job(id: 1) {
#             employer {
#                 name
#                 jobs {
#                     title
#                 }
#             }
#         }
#     }
#     """
#     response = test_client.post(graphql_endpoint, json={"query": query})
#     assert response is not None
#     assert response.status_code == 200

#     result = response.json()
#     job = result["data"]["job"]
#     assert job["employer"]["name"] == EMPLOYERS_DATA[0]["name"]
#     employer_jobs = job["employer"]["jobs"]
#     assert len(employer_jobs) == 2
#     assert sorted([job["title"] for job in employer_jobs]) == sorted(
#         [job["title"] for job in JOBS_DATA[:2]]
#     )

#     # Should not pass.
#     query = """
#     query {
#         job(id: 1) {
#             employer {
#                 name
#                 jobs {
#                     employer {
#                         name
#                     }
#                 }
#             }
#         }
#     }
#     """
#     response = test_client.post(graphql_endpoint, json={"query": query})
#     assert response is not None
#     assert response.status_code == 200

#     result = response.json()
#     assert result["data"]["job"] is None
#     assert len(result["errors"]) >= 1


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
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    users = result["data"]["users"]
    assert len(users) == len(USERS_DATA)
    assert sorted([user["username"] for user in users]) == sorted(
        user["username"] for user in USERS_DATA
    )
    for user in users:
        assert "password" not in user


@pytest.mark.api
@pytest.mark.query
def test_get_all_applications(test_client, graphql_endpoint):
    #     job {
    #     id
    # }
    # user {
    #     id
    # }
    query = """
    query {
        applications {
            jobId
            userId
        }
    }
    """
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    applications = result["data"]["applications"]
    assert len(applications) == len(APPLICATIONS_DATA)

    # Testing correct relationship retrieval.
    # for application in applications:
    #     assert application["jobId"] == application["job"]["id"]
    #     assert application["userId"] == application["user"]["id"]
