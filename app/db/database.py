from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.models import Base
from app.settings.config import DATABASE_URL
from app.tests.utils import load_test_tables

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
        load_test_tables(session)
        session.commit()
