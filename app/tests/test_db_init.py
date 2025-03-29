from sqlalchemy.orm import joinedload
from app.db.models import (
    Job as Job_sql,
    Employer as Employer_sql,
)
from app.db.data import JOBS_DATA, EMPLOYERS_DATA


def test_jobs_query(db_session):
    # Query jobs with their employers
    jobs = db_session.query(Job_sql).options(joinedload(Job_sql.employer)).all()

    # Job assertions
    assert len(jobs) == len(JOBS_DATA)
    assert jobs[0].title == JOBS_DATA[0]["title"]
    assert jobs[0].employer.name == EMPLOYERS_DATA[0]["name"]

    # Query employers and their posted jobs.
    employers = (
        db_session.query(Employer_sql).options(joinedload(Employer_sql.jobs)).all()
    )

    # Employer assertions.
    assert len(employers) == len(EMPLOYERS_DATA)
    assert (employers[0].name) == EMPLOYERS_DATA[0]["name"]
    assert len(employers[0].jobs) == len(
        [job for job in JOBS_DATA if job["employer_id"] == 1]
    )
