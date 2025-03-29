import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from app.db.data import EMPLOYERS_DATA, JOBS_DATA
from app.db.models import Base, Employer as Employer_sql, Job as Job_sql


# Assumption: Docker container containing test db has to be running
# prior to the test being run.
def pytest_addoption(parser):
    parser.addoption(
        "--dburl",
        action="store",
        help="Test DB URL.",
        default="postgresql+psycopg://test_user:test_pass@localhost:5433/test_db",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db_url = session.config.getoption("--dburl")
    try:
        engine = create_engine(
            db_url,
            poolclass=StaticPool,
        )
        connection = engine.connect()
        connection.close()
        print("Database connection successful")
    except SQLAlchemyOperationalError as e:
        print(f"Failed to connect to the database at {db_url}: {e}")
        pytest.exit("Database connection could not be established")


@pytest.fixture(scope="session")
def db_url(request):
    return request.config.getoption("--dburl")


@pytest.fixture(scope="function")
def db_session(db_url):
    engine = create_engine(
        db_url,
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables in the database.
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Initialise test db.
    session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
    session.flush()
    session.add_all([Job_sql(**x) for x in JOBS_DATA])
    session.flush()

    yield session

    Base.metadata.drop_all(bind=engine)
    session.close()
    transaction.rollback()
    connection.close()
