import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from .utils import post_graphql
from app.db.repositories.application_repository import ApplicationRepository


@pytest.mark.api
@pytest.mark.mutation
def test_add_job(
    test_client,
    graphql_endpoint,
    admin_header,
):
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)

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
def test_successfully_update_existing_job_title(
    test_client,
    graphql_endpoint,
    admin_header,
):
    updated_title = "Improved job title"
    query = f"""
    mutation {{
        updateJob(jobId: 1, title: "{updated_title}") {{
            id
            title
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    job = result["data"]["updateJob"]
    assert job["id"] == 1
    assert job["title"] == updated_title


@pytest.mark.api
@pytest.mark.mutation
def test_successfully_update_existing_job_employer(
    test_client,
    graphql_endpoint,
    admin_header,
):
    updated_employer_id = 2
    query = f"""
    mutation {{
        updateJob(jobId: 1, employerId: {updated_employer_id}) {{
            id
            title
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
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
def test_update_nonexisting_job(
    test_client,
    graphql_endpoint,
    admin_header,
):
    updated_title = "Improved job title"
    query = f"""
    mutation {{
        updateJob(jobId: 14, title: "{updated_title}") {{
            id
            title
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    assert result["data"] is None
    assert "errors" in result
    assert "not found" in result["errors"][0]["message"]


@pytest.mark.api
@pytest.mark.mutation
def test_delete_existing_job(
    test_client,
    db_session,
    graphql_endpoint,
    admin_header,
):
    job_id = 1
    query = f"""
    mutation {{
        deleteJob(jobId: {job_id})
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    assert result["data"]["deleteJob"]

    # Check that the job has actually been deleted.
    query = f"""
    query {{
        job(id: {job_id}) {{
            title
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert result["data"]["job"] is None

    # Test cascade delete on applications.
    applications = ApplicationRepository.get_all_applications_by_job_id(
        db_session=db_session, selected_fields="", job_id=job_id, gql=False
    )
    for application in applications:
        assert application.job_id != job_id
