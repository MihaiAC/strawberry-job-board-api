import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from .test_utils import post_graphql


@pytest.mark.api
@pytest.mark.mutation
def test_add_employer_complete_info(test_client, graphql_endpoint):
    employer_name = "X name"
    employer_industry = "YZ industry"
    employer_email = "XYZ@example.com"
    query = f"""
    mutation {{
        addEmployer(name: "{employer_name}", industry: "{employer_industry}" contactEmail: "{employer_email}") {{
            id
            name
            industry
            contactEmail
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employer = result["data"]["addEmployer"]
    assert employer["id"] == len(EMPLOYERS_DATA) + 1
    assert employer["name"] == employer_name
    assert employer["industry"] == employer_industry
    assert employer["contactEmail"] == employer_email


@pytest.mark.api
@pytest.mark.mutation
def test_successfully_update_existing_employer_name(test_client, graphql_endpoint):
    updated_name = "Updatio Updatius"
    query = f"""
    mutation {{
        updateEmployer(employerId: 1, name: "{updated_name}") {{
            id
            name
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employer = result["data"]["updateEmployer"]
    assert employer["id"] == 1
    assert employer["name"] == updated_name


@pytest.mark.api
@pytest.mark.mutation
def test_update_nonexisting_employer(test_client, graphql_endpoint):
    updated_name = "Updatio Updatius"
    query = f"""
    mutation {{
        updateEmployer(employerId: 10, name: "{updated_name}") {{
            id
            name
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"] is None
    assert "errors" in result
    assert "not found" in result["errors"][0]["message"]


@pytest.mark.api
@pytest.mark.mutation
def test_update_existing_employer_insufficient_args(test_client, graphql_endpoint):
    query = """
    mutation {
        updateEmployer(employerId: 1) {
            id
            name
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"] is None
    assert "errors" in result
    assert (
        "Please provide at least one employer field you would like to modify."
        == result["errors"][0]["message"]
    )


@pytest.mark.api
@pytest.mark.mutation
def test_delete_existing_employer(test_client, graphql_endpoint):
    query = """
    mutation {
        deleteEmployer(employerId: 1)
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"]["deleteEmployer"]

    # Check that the job has actually been deleted.
    query = """
    query {
        employer(id: 1) {
            name
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"]["employer"] is None

    # Test cascade deletes.
    query = """
    query {
        jobs {
            id
            employerId
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    remaining_job_ids = []
    jobs = result["data"]["jobs"]
    for job in jobs:
        assert job["employerId"] != 1
        remaining_job_ids.append(job["id"])

    query = """
    query {
        applications {
            id
            jobId
            userId
        }
    }
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    applications = result["data"]["applications"]
    for application in applications:
        assert application["jobId"] in remaining_job_ids


@pytest.mark.api
@pytest.mark.mutation
def test_add_jobs_to_new_employer(test_client, graphql_endpoint):
    employer_name = "X name"
    employer_industry = "YZ industry"
    employer_email = "XYZ@example.com"
    new_employer_id = len(EMPLOYERS_DATA) + 1
    query = f"""
    mutation {{
        addEmployer(name: "{employer_name}", industry: "{employer_industry}" contactEmail: "{employer_email}") {{
            id
            name
            industry
            contactEmail
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    employer = result["data"]["addEmployer"]
    assert employer["id"] == new_employer_id

    # Add a new job to the new employer.
    query = f"""
    mutation {{
        addJob(title: "X title", description: "X descr", employerId: {new_employer_id}) {{
            id
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["addJob"]
    assert job["id"] == len(JOBS_DATA) + 1

    # Change an existing job's employer to be the new employer.
    query = f"""
    mutation {{
        updateJob(jobId: 1, employerId: {new_employer_id}) {{
            id
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    job = result["data"]["updateJob"]
    assert job["id"] == 1

    # Retrieve the jobs of the new employer.
    query = f"""
    query {{
        employer(id: {new_employer_id}) {{
            jobs {{
                id
            }}
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    jobs = result["data"]["employer"]["jobs"]
    assert len(jobs) == 2
    assert sorted([job["id"] for job in jobs]) == [1, len(JOBS_DATA) + 1]
