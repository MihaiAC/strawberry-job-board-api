import strawberry
from .employer.mutations import EmployerMutation
from .job.mutations import JobMutation
from .user.mutations import LoginMutation, UserMutation
from .application.mutations import ApplicationMutation


@strawberry.type
class Mutation(
    EmployerMutation,
    JobMutation,
    LoginMutation,
    UserMutation,
    ApplicationMutation,
):
    pass
