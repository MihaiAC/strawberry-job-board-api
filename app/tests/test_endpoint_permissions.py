import pytest
from .utils import BaseQueries, post_graphql


@pytest.mark.auth
@pytest.mark.parametrize(
    "query, permissions",
    [
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
    ],
)
def test_permissions(
    test_client, graphql_endpoint, user_header, admin_header, query, permissions
):
    # unauth_has_permission, user_has_permission, admin_has_permission
    # = permissions

    for idx, header in enumerate(["", user_header, admin_header]):
        result = post_graphql(test_client, graphql_endpoint, query, headers=header)
        has_permission = permissions[idx]
        query_was_successful = "errors" not in result
        assert (
            has_permission == query_was_successful
        ), f"{idx} {has_permission} {query_was_successful}"
