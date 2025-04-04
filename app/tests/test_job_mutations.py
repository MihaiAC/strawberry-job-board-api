import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from .utils import post_graphql


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
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)

    job = result["data"]["addJob"]
    assert job["id"] == len(JOBS_DATA) + 1
    assert job["title"] == "X title"
    assert job["description"] == "X descr"

    query = f"""
    query {{
        job(id: {len(JOBS_DATA)+1}) {{
            employer {{
                name
            }}
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["job"]
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
    result = post_graphql(test_client, graphql_endpoint, query)
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
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["updateJob"]
    assert job["id"] == 1

    # Test that SQLA relationship has been successfully updated.
    query = """
    query {
        job(id: 1) {
            employer {
                id
            }
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["job"]
    assert job["employer"]["id"] == updated_employer_id

    query = f"""
    query {{
        employer(id: {updated_employer_id}) {{
            jobs {{
                id
            }}
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    jobs = result["data"]["employer"]["jobs"]
    assert 1 in [job["id"] for job in jobs]


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
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"] is None
    assert "errors" in result
    assert "not found" in result["errors"][0]["message"]


@pytest.mark.api
@pytest.mark.mutation
def test_delete_existing_job(test_client, graphql_endpoint):
    query = """
    mutation {
        deleteJob(jobId: 1)
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"]["deleteJob"]

    # Check that the job has actually been deleted.
    query = """
    query {
        job(id: 1) {
            title
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"]["job"] is None

    # Test cascade delete on applications.
    query = """
    query {
        applications {
            id
            jobId
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    for application in result["data"]["applications"]:
        assert application["jobId"] != 1
