from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.models import (
    Base,
    Employer as Employer_sql,
    Job as Job_sql,
    User as User_sql,
    Application as Application_sql,
)
from app.settings.config import DATABASE_URL
from app.db.data import EMPLOYERS_DATA, JOBS_DATA, USERS_DATA, APPLICATIONS_DATA

# Create engine.
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


# Drop tables on rerun.
def prepare_database():
    """
    Runs on application start.
    Drops previous tables and loads in dummy data.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
        session.add_all([Job_sql(**x) for x in JOBS_DATA])
        session.add_all([User_sql(**x) for x in USERS_DATA])
        session.add_all([Application_sql(**x) for x in APPLICATIONS_DATA])
        session.commit()
