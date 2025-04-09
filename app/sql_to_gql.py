from .db.models import (
    Employer as Employer_sql,
    Job as Job_sql,
    User as User_sql,
    Application as Application_sql,
)
from .gql.types import (
    Employer_gql,
    Job_gql,
    User_gql,
    Application_gql,
)


# TODO: Boilerplate to avoid circular imports.
def employer_to_gql(employer_sql: Employer_sql) -> Employer_gql:
    return Employer_gql(
        id=employer_sql.id,
        name=employer_sql.name,
        contact_email=employer_sql.contact_email,
        industry=employer_sql.industry,
    )


def job_to_gql(job_sql: Job_sql) -> Job_gql:
    return Job_gql(
        id=job_sql.id,
        title=job_sql.title,
        description=job_sql.description,
        employer_id=job_sql.employer_id,
    )


def application_to_gql(application_sql: Application_sql) -> Application_gql:
    return Application_gql(
        id=application_sql.id,
        user_id=application_sql.user_id,
        job_id=application_sql.job_id,
    )


def user_to_gql(user_sql: User_sql) -> User_gql:
    return User_gql(
        id=user_sql.id,
        username=user_sql.username,
        email=user_sql.email,
        role=user_sql.role,
    )
