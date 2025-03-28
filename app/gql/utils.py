from .types import (
    Job as Job_gql,
    Employer as Employer_gql,
)
from app.db.database import (
    Employer_sql,
    Job_sql,
)


# Handling circular references.
def to_job_gql(job: Job_sql, deep: bool = False) -> Job_gql:
    return Job_gql(
        id=job.id,
        title=job.title,
        description=job.description,
        employer_id=job.employer_id,
        employer=(
            to_employer_gql(job.employer, deep=deep) if deep and job.employer else None
        ),
    )


def to_employer_gql(employer: Employer_sql, deep: bool = False) -> Employer_gql:
    return Employer_gql(
        id=employer.id,
        name=employer.name,
        contact_email=employer.contact_email,
        industry=employer.industry,
        jobs=[to_job_gql(job, deep=False) for job in employer.jobs] if deep else [],
    )
