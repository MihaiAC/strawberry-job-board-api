import pytest
from app.db.data import JOBS_DATA


@pytest.mark.api
@pytest.mark.integration
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
