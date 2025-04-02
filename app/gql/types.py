import strawberry
from typing import List, Optional


class Base_gql:
    pass


@strawberry.type
class Employer_gql(Base_gql):
    id: int
    name: str
    contact_email: str
    industry: str
    jobs: Optional[List["Job_gql"]]


@strawberry.type
class Job_gql(Base_gql):
    id: int
    title: str
    description: str
    employer_id: int
    employer: Optional[Employer_gql]
    applications: Optional[List["Application_gql"]]


@strawberry.type
class User_gql(Base_gql):
    id: int
    username: str
    email: str
    role: str
    applications: Optional[List["Application_gql"]]


@strawberry.type
class Application_gql(Base_gql):
    id: int
    user_id: int
    job_id: int
    user: Optional[User_gql]
    job: Optional[Job_gql]
