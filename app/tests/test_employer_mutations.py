import pytest
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from .utils import post_graphql
from app.db.repositories.employer_repository import EmployerRepository
from app.db.repositories.job_repository import JobRepository
from app.db.repositories.application_repository import ApplicationRepository
from app.errors.error_messages import EMPLOYER_ALREADY_EXISTS
from app.errors.custom_errors import ResourceNotFound


@pytest.mark.api
@pytest.mark.mutation
def test_add_employer_complete_info(
    test_client,
    graphql_endpoint,
    admin_header,
):
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    employer = result["data"]["addEmployer"]
    assert employer["id"] == len(EMPLOYERS_DATA) + 1
    assert employer["name"] == employer_name
    assert employer["industry"] == employer_industry
    assert employer["contactEmail"] == employer_email


@pytest.mark.api
@pytest.mark.mutation
def test_add_employer_existing_email(
    test_client,
    graphql_endpoint,
    admin_header,
):
    employer_name = "X name"
    employer_industry = "YZ industry"
    employer_email = EMPLOYERS_DATA[0]["contact_email"]
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    assert "errors" in result
    assert result["errors"][0]["message"] == EMPLOYER_ALREADY_EXISTS


@pytest.mark.api
@pytest.mark.mutation
def test_successfully_update_existing_employer_name(
    test_client,
    graphql_endpoint,
    admin_header,
):
    updated_name = "Updatio Updatius"
    query = f"""
    mutation {{
        updateEmployer(employerId: 1, name: "{updated_name}") {{
            id
            name
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    employer = result["data"]["updateEmployer"]
    assert employer["id"] == 1
    assert employer["name"] == updated_name


@pytest.mark.api
@pytest.mark.mutation
def test_update_nonexisting_employer(
    test_client,
    graphql_endpoint,
    admin_header,
):
    updated_name = "Updatio Updatius"
    query = f"""
    mutation {{
        updateEmployer(employerId: 10, name: "{updated_name}") {{
            id
            name
        }}
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    assert result["data"] is None
    assert "errors" in result
    assert result["errors"][0]["message"] == ResourceNotFound.get_message("Employer")


@pytest.mark.api
@pytest.mark.mutation
def test_delete_existing_employer(
    test_client,
    graphql_endpoint,
    db_session,
    admin_header,
):
    employer_id = 1
    query = f"""
    mutation {{
        deleteEmployer(employerId: {employer_id})
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    assert result["data"]["deleteEmployer"]

    # Check that the employer has actually been deleted.
    employer = EmployerRepository.get_employer_by_id(
        db_session=db_session,
        id=employer_id,
        gql=False,
    )
    assert employer is None

    # Check that the jobs belonging to the employer have been deleted.
    jobs = JobRepository.get_all_jobs(
        db_session=db_session,
        gql=False,
    )
    remaining_job_ids = []
    for job_sql in jobs:
        assert job_sql.employer_id != employer_id
        remaining_job_ids.append(job_sql.id)

    # Check that the applications corresponding to the deleted jobs
    # have been deleted.
    remaining_applications = ApplicationRepository.get_all_applications(
        db_session=db_session, gql=False
    )
    for application in remaining_applications:
        assert application.job_id in remaining_job_ids


@pytest.mark.api
@pytest.mark.mutation
def test_add_jobs_to_new_employer(
    test_client,
    graphql_endpoint,
    admin_header,
):
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
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
    result = post_graphql(test_client, graphql_endpoint, query, headers=admin_header)
    jobs = result["data"]["employer"]["jobs"]
    assert len(jobs) == 2
    assert sorted([job["id"] for job in jobs]) == [1, len(JOBS_DATA) + 1]
