from sqlalchemy import create_engine
from app.db.models import Base

engine = create_engine("sqlite:///temp.db")
Base.metadata.create_all(engine)
