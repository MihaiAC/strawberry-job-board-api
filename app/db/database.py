from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.models import (
    Base,
    Employer as Employer_sql,
    Job as Job_sql,
)
from app.settings.config import DATABASE_URL
from app.db.data import EMPLOYERS_DATA, JOBS_DATA

# Create engine.
engine = create_engine(DATABASE_URL, echo=True)


# Drop tables on rerun.
def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all([Employer_sql(**x) for x in EMPLOYERS_DATA])
        session.add_all([Job_sql(**x) for x in JOBS_DATA])
        session.commit()
