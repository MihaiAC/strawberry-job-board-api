import strawberry
from .employer.queries import EmployerQuery
from .job.queries import JobQuery
from .user.queries import UserQuery
from .application.queries import ApplicationQuery


@strawberry.type
class Query(EmployerQuery, JobQuery, UserQuery, ApplicationQuery):
    pass
