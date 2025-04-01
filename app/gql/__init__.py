import strawberry
from .employer.mutations import EmployerMutation
from .employer.queries import EmployerQuery
from .job.mutations import JobMutation
from .job.queries import JobQuery
from .user.queries import UserQuery
from .application.queries import ApplicationQuery


@strawberry.type
class Query(EmployerQuery, JobQuery, UserQuery, ApplicationQuery):
    pass


@strawberry.type
class Mutation(EmployerMutation, JobMutation):
    pass
