import pytest
from sqlalchemy import create_engine
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from sqlalchemy.orm import sessionmaker, scoped_session
from app.settings.config import TEST_DATABASE_URL
from app.db.models import Base, Employer as Employer_sql, Job as Job_sql


@pytest.fixture(scope="function")
def db_session(postgresql):
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))

    session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
    session.flush()

    session.add_all([Job_sql(**x) for x in JOBS_DATA])
    session.commit()

    yield session

    # Base.metadata.drop_all(engine)
    session.close()
    # engine.dispose()
