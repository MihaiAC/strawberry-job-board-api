from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    # Not a true role in the sense that user.role can only be "user" or "admin".
    # Used to give an explicit role to an unauthenticated request.
    UNAUTHENTICATED = "unauthenticated"
