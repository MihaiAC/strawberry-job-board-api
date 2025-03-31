import strawberry
from strawberry.types import Info
from app.gql.types import Employer as Employer_gql
from app.db.database import Employer_sql
from app.gql.utils import to_employer_gql


@strawberry.type
class EmployerMutation:

    @strawberry.mutation
    def add_employer(
        self,
        name: str,
        contact_email: str,
        industry: str,
        info: Info,
    ) -> Employer_gql:
        db_session = info.context["db_session"]
        employer_sql = Employer_sql(
            name=name, contact_email=contact_email, industry=industry
        )
        db_session.add(employer_sql)
        db_session.commit()
        db_session.refresh(employer_sql)

        employer_gql = to_employer_gql(employer_sql, deep=True)
        return employer_gql
