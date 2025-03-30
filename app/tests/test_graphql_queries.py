import pytest
from app.db.data import JOBS_DATA, EMPLOYERS_DATA


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
