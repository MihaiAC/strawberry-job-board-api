from app.auth_utils import (
    generate_jwt_token,
    decode_jwt_token_return_email,
    hash_password,
    verify_password,
)
import pytest
from freezegun import freeze_time
from graphql import GraphQLError


@pytest.mark.auth
def test_hash_password():
    test_password = "abc123"
    password_hash = hash_password(test_password)

    # Test correct password returns True.
    assert verify_password(password_hash, test_password)

    # Test incorrect password throws error.
    with pytest.raises(GraphQLError):
        assert verify_password(password_hash, "incorrectpass")


@pytest.mark.auth
def test_jwt_encode_decode():
    email = "abc@example.com"
    with freeze_time("2025-04-03 12:00:00"):
        token = generate_jwt_token(email)

    # Token still fresh.
    with freeze_time("2025-04-03 12:10:00"):
        assert email == decode_jwt_token_return_email(token)

    # Token expired.
    with freeze_time("2025-04-03 12:15:01"):
        with pytest.raises(GraphQLError):
            decode_jwt_token_return_email(token)
