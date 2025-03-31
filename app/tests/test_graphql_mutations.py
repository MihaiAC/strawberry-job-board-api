import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA


@pytest.mark.api
@pytest.mark.mutation
def test_add_job(test_client, graphql_endpoint):
    bla = True
    assert bla
    query = """
    mutation {
        addJob(title: "X title", description: "X descr", employerId: 1) {
            id
            title
            description
            employerId
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
    job = result["data"]["addJob"]
    assert job["id"] == len(JOBS_DATA) + 1
    assert job["title"] == "X title"
    assert job["description"] == "X descr"

    assert job["employer"]["name"] == EMPLOYERS_DATA[0]["name"]
