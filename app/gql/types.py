import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.auth.auth_utils import require_role
from app.auth.roles import Role
from app.sql_to_gql import employer_to_gql, job_to_gql, application_to_gql


class Base_gql:
    pass


@strawberry.type
class Employer_gql(Base_gql):
    id: int
    name: str
    contact_email: str
    industry: str

    @strawberry.field
    async def jobs(self, info: Info) -> List["Job_gql"]:
        loader = info.context["loaders"]["jobs_from_employer"]
        jobs_sql = await loader.load(self.id)
        return [job_to_gql(job) for job in jobs_sql]


@strawberry.type
class Job_gql(Base_gql):
    id: int
    title: str
    description: str
    employer_id: int

    @strawberry.field
    async def employer(self, info: Info) -> Optional[Employer_gql]:
        loader = info.context["loaders"]["employer_from_jobs"]
        employer_sql = await loader.load(self.employer_id)
        return employer_to_gql(employer_sql)

    @strawberry.field
    @require_role([Role.USER, Role.ADMIN, Role.UNAUTHENTICATED])
    async def applications(self, info: Info) -> List["Application_gql"]:
        user = info.context["user"]
        if user is None:
            return []

        if user.role == Role.USER:
            loader = info.context["loaders"]["user_applications_from_job"]
            applications_sql = await loader.load((self.id, user.id))
        elif user.role == Role.ADMIN:
            loader = info.context["loaders"]["all_applications_from_job"]
            applications_sql = await loader.load(self.id)
        else:
            return []
        return [application_to_gql(app) for app in applications_sql]


@strawberry.type
class User_gql(Base_gql):
    id: int
    username: str
    email: str
    role: str

    @strawberry.field
    @require_role([Role.USER, Role.ADMIN, Role.UNAUTHENTICATED])
    async def applications(self, info: Info) -> List["Application_gql"]:
        # Only retrieve applications if request user matches this user
        # or the user is an admin.
        user = info.context["user"]

        if user is None or (user.role != Role.ADMIN and user.id != self.id):
            return []
        loader = info.context["loaders"]["applications_from_user"]
        applications_sql = await loader.load(self.id)

        return [application_to_gql(app) for app in applications_sql]


@strawberry.type
class Application_gql(Base_gql):
    id: int
    user_id: int
    job_id: int

    @strawberry.field
    async def user(self, info: Info) -> Optional[User_gql]:
        return None

    @strawberry.field
    async def job(self, info: Info) -> Optional[Job_gql]:
        return None
