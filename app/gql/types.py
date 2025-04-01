import strawberry
from typing import List


# Way to handle circular references.
@strawberry.type
class Employer:
    id: int
    name: str
    contact_email: str
    industry: str
    jobs: List["Job"]


@strawberry.type
class Job:
    id: int
    title: str
    description: str
    employer_id: int
    employer: Employer
    applications: List["Application"]


@strawberry.type
class User:
    id: int
    username: str
    email: str
    role: str
    applications: List["Application"]


@strawberry.type
class Application:
    id: int
    user_id: int
    job_id: int
    user: User
    job: Job


@strawberry.type
class Success:
    success: bool
    message: str
