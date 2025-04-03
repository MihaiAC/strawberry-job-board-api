import strawberry
from .employer.mutations import EmployerMutation
from .job.mutations import JobMutation
from .user.mutations import LoginMutation, UserMutation


@strawberry.type
class Mutation(EmployerMutation, JobMutation, LoginMutation, UserMutation):
    pass
