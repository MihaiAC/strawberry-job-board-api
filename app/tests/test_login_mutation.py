import pytest
from app.db.data import USERS_DATA
from .utils import post_graphql
from app.auth.auth_utils import decode_jwt_token_return_email
from app.errors.error_messages import INVALID_PASSWORD
from app.errors.custom_errors import ResourceNotFound


@pytest.mark.api
@pytest.mark.mutation
def test_login_correct_details(test_client, graphql_endpoint):
    user_email = USERS_DATA[0]["email"]
    user_password = USERS_DATA[0]["password"]
    query = f"""
    mutation {{
        loginUser(email: "{user_email}", password: "{user_password}")
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert "errors" not in result
    assert "loginUser" in result["data"]

    jwt_token = result["data"]["loginUser"]
    assert jwt_token is not None and len(jwt_token) > 0
    assert user_email == decode_jwt_token_return_email(jwt_token)


@pytest.mark.api
@pytest.mark.mutation
def test_login_incorrect_email(test_client, graphql_endpoint):
    user_email = "random_email@example.com"
    user_password = USERS_DATA[0]["password"]
    query = f"""
    mutation {{
        loginUser(email: "{user_email}", password: "{user_password}")
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert "errors" in result
    error_msgs = [error["message"] for error in result["errors"]]
    assert ResourceNotFound.get_message("User") in error_msgs


@pytest.mark.api
@pytest.mark.mutation
def test_login_incorrect_password(test_client, graphql_endpoint):
    user_email = USERS_DATA[0]["email"]
    user_password = "xyz"
    query = f"""
    mutation {{
        loginUser(email: "{user_email}", password: "{user_password}")
    }}
    """
    result = post_graphql(test_client, graphql_endpoint, query)
    assert "errors" in result
    error_msgs = [error["message"] for error in result["errors"]]
    assert INVALID_PASSWORD in error_msgs
