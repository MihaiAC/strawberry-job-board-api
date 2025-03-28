import pytest
from sqlalchemy.orm import joinedload
from app.db.models import Job as Job_sql
from app.db.data import JOBS_DATA


def test_jobs_query(db_session):
    # Query jobs with their employers
    jobs = db_session.query(Job_sql).options(joinedload(Job_sql.employer)).all()

    # Assertions
    assert len(jobs) == len(JOBS_DATA)
    assert jobs[0].title == "Tester"
    assert jobs[0].employer.name == "Test Inc"
