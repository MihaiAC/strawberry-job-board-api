import strawberry
from .employer.mutations import EmployerMutation
from .job.mutations import JobMutation
from .user.mutations import LoginMutation


@strawberry.type
class Mutation(EmployerMutation, JobMutation, LoginMutation):
    pass
