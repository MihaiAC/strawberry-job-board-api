import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA


@pytest.mark.api
@pytest.mark.mutation
def test_add_job(test_client, graphql_endpoint):
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


@pytest.mark.api
@pytest.mark.mutation
def test_successfully_update_existing_job_title(test_client, graphql_endpoint):
    updated_title = "Improved job title"
    query = f"""
    mutation {{
        updateJob(jobId: 1, title: "{updated_title}") {{
            id
            title
        }}
    }}
    """

    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    job = result["data"]["updateJob"]
    assert job["id"] == 1
    assert job["title"] == updated_title


@pytest.mark.api
@pytest.mark.mutation
def test_successfully_update_existing_job_employer(test_client, graphql_endpoint):
    updated_employer_id = 2
    query = f"""
    mutation {{
        updateJob(jobId: 1, employerId: {updated_employer_id}) {{
            id
            title
            employer {{
                id
            }}
        }}
    }}
    """
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    job = result["data"]["updateJob"]
    assert job["id"] == 1
    assert job["employer"]["id"] == updated_employer_id


@pytest.mark.api
@pytest.mark.mutation
def test_update_nonexisting_job(test_client, graphql_endpoint):
    updated_title = "Improved job title"
    query = f"""
    mutation {{
        updateJob(jobId: 14, title: "{updated_title}") {{
            id
            title
        }}
    }}
    """

    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    assert result["data"] is None
    assert "errors" in result
    assert "not found" in result["errors"][0]["message"]


@pytest.mark.api
@pytest.mark.mutation
def test_update_existing_job_insufficient_args(test_client, graphql_endpoint):
    query = """
    mutation {
        updateJob(jobId: 1) {
            id
            title
        }
    }
    """
    response = test_client.post(graphql_endpoint, json={"query": query})
    assert response is not None
    assert response.status_code == 200

    result = response.json()
    assert result["data"] is None
    assert "errors" in result
    assert (
        "Please provide at least one job field you would like to modify."
        == result["errors"][0]["message"]
    )
