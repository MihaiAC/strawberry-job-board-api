import strawberry
from .employer.mutations import EmployerMutation
from .job.mutations import JobMutation


@strawberry.type
class Mutation(EmployerMutation, JobMutation):
    pass
