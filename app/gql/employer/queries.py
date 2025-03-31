import strawberry
from strawberry.types import Info
from typing import List, Optional
from app.gql.types import Employer as Employer_gql
from app.db.database import Employer_sql
from sqlalchemy.orm import joinedload
from app.gql.utils import to_employer_gql


@strawberry.type
class EmployerQuery:
    # Allow retrieval of an employer's jobs.
    # Disallow retrieval of the employer's jobs' employer
    # (not useful anyway, since a job can't have multiple employers).
    @strawberry.field
    def employers(self, info: Info) -> List[Employer_gql]:
        db_session = info.context["db_session"]
        employers = (
            db_session.query(Employer_sql).options(joinedload(Employer_sql.jobs)).all()
        )
        return [to_employer_gql(employer, deep=True) for employer in employers]

    @strawberry.field
    def employer(self, id: int, info: Info) -> Optional[Employer_gql]:
        db_session = info.context["db_session"]
        employer = (
            db_session.query(Employer_sql)
            .options(joinedload(Employer_sql.jobs))
            .filter_by(id=id)
            .first()
        )
        return to_employer_gql(employer, deep=True) if employer else None
