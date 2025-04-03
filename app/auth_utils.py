import jwt
from datetime import datetime, timedelta, timezone
from app.settings.config import JWT_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES
from graphql import GraphQLError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def generate_jwt_token(email: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(JWT_EXPIRATION_TIME_MINUTES)
    )

    payload = {
        "sub": email,
        "exp": expiration_time,
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
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")
