import pytest
from .utils import BaseQueries, post_graphql
from app.auth.roles import Role


# TODO: Maybe should add token expiration tests here.


def generate_permission_tests():
    cases = [
        (BaseQueries.APPLICATIONS, [False, True, True]),
        (BaseQueries.LOGIN, [True, False, False]),
        (BaseQueries.UPDATE_EMPLOYER, [False, False, True]),
        (BaseQueries.ADD_EMPLOYER, [False, False, True]),
        (BaseQueries.DELETE_EMPLOYER, [False, False, True]),
        (BaseQueries.ADD_JOB, [False, False, True]),
        (BaseQueries.UPDATE_JOB, [False, False, True]),
        (BaseQueries.DELETE_JOB, [False, False, True]),
        (BaseQueries.QUERY_ALL_JOBS, [True, True, True]),
        (BaseQueries.QUERY_JOB_BY_ID, [True, True, True]),
        (BaseQueries.QUERY_ALL_USERS, [False, True, True]),
        (BaseQueries.CREATE_APPLICATION, [False, True, False]),
        (BaseQueries.ADD_USER, [True, False, True]),
    ]

    for query, (unauth, user, admin) in cases:
        yield (query, Role.UNAUTHENTICATED, unauth)
        yield (query, Role.USER, user)
        yield (query, Role.ADMIN, admin)


@pytest.mark.auth
@pytest.mark.parametrize(
    "query, role, expected_permission",
    generate_permission_tests(),
)
def test_permissions(
    test_client,
    graphql_endpoint,
    user_header,
    admin_header,
    query,
    role,
    expected_permission,
):
    # Set headers.
    if role == Role.UNAUTHENTICATED:
        headers = ""
    elif role == Role.USER:
        headers = user_header
    elif role == Role.ADMIN:
        headers = admin_header
    else:
        pytest.fail(f"Unknown role {role}")

    result = post_graphql(test_client, graphql_endpoint, query, headers=headers)
    query_successful = "errors" not in result
    assert (
        query_successful == expected_permission
    ), f"{role} access for query {query} expected {expected_permission} but got {query_successful}"
