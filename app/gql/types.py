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
