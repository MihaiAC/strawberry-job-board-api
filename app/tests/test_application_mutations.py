import pytest
from app.db.data import APPLICATIONS_DATA, JOBS_DATA
from .utils import post_graphql, get_job_ids_for_user, get_test_first_non_admin_id
from app.errors.error_messages import ALREADY_APPLIED
from app.errors.custom_errors import ResourceNotFound
from app.db.repositories.application_repository import ApplicationRepository


def assert_no_new_application_added(db_session):
    applications = ApplicationRepository.get_all_applications(
        db_session=db_session,
        gql=False,
    )
    assert len(applications) == len(APPLICATIONS_DATA)


@pytest.mark.api
@pytest.mark.mutation
@pytest.mark.auth
def test_add_new_application(test_client, graphql_endpoint, user_header):
    user_id = get_test_first_non_admin_id()
    job_id = get_job_ids_for_user(user_id, applied=False)[0]

    query = f"""
        mutation {{
            applyToJob(jobId: {job_id})
        }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    assert "errors" not in result
    assert result["data"]["applyToJob"]

    # Test that application has been added.
    query = """
        query {
            applications {
                jobId
                userId
                id
            }
        }
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    assert "errors" not in result
    applications = result["data"]["applications"]
    found_new_application = False
    for application in applications:
        if application["id"] == len(APPLICATIONS_DATA) + 1:
            found_new_application = True
            assert job_id == application["jobId"]
            assert user_id == application["userId"]
    assert found_new_application


@pytest.mark.api
@pytest.mark.mutation
@pytest.mark.auth
def test_add_existing_application(test_client, graphql_endpoint, user_header):
    user_id = get_test_first_non_admin_id()
    job_id = get_job_ids_for_user(user_id, applied=True)[0]

    query = f"""
        mutation {{
            applyToJob(jobId: {job_id})
        }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    assert "errors" in result
    assert result["errors"][0]["message"] == ALREADY_APPLIED


@pytest.mark.api
@pytest.mark.mutation
@pytest.mark.auth
def test_add_application_to_nonexistent_job(test_client, graphql_endpoint, user_header):
    job_id = len(JOBS_DATA) + 1

    query = f"""
        mutation {{
            applyToJob(jobId: {job_id})
        }}
    """
    result = post_graphql(test_client, graphql_endpoint, query, headers=user_header)
    assert "errors" in result
    assert result["errors"][0]["message"] == ResourceNotFound.get_message("Job")
