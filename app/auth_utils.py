import jwt
from jwt.exceptions import InvalidSignatureError
from datetime import datetime, timedelta, timezone
from app.settings.config import JWT_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES
from graphql import GraphQLError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Request


def generate_jwt_token(email: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(JWT_EXPIRATION_TIME_MINUTES)
    )

    payload = {
        "email": email,
        "expiration_time": expiration_time.timestamp(),
    }

    token = jwt.encode(payload, JWT_KEY, algorithm=JWT_ALGORITHM)
    return token


def hash_password(password: str) -> str:
    hasher = PasswordHasher()
    return hasher.hash(password)


def verify_password(stored_hash: str, input_password: str) -> bool:
    hasher = PasswordHasher()
    try:
        hasher.verify(stored_hash, input_password)
        return True
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def extract_token_from_request(request: Request) -> str:
    """
    Args:
        request (Request): The FastAPI request object containing the
        Authorization header.
    Returns:
        str: The JWT contained in the request header.
    Raises:
        GraphQLError: If Authorization header or the token is missing.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise GraphQLError("Authorization header missing or invalid.")
    jwt_token = auth_header[7:]
    return jwt_token


def decode_jwt_token_return_email(jwt_token: str) -> str:
    """
    Returns:
        str: The email address of the user, decoded from the JWT token.

    Raises:
        GraphQLError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(jwt_token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        if datetime.now(timezone.utc) > datetime.fromtimestamp(
            payload["expiration_time"], tz=timezone.utc
        ):
            raise GraphQLError("Token has expired.")
        return payload["email"]
    except InvalidSignatureError:
        raise GraphQLError("Invalid authentication token.")


def get_user_email_from_request_token(request: Request) -> str:
    token = extract_token_from_request(request)
    email = decode_jwt_token_return_email(token)
    return email
