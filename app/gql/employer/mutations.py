import strawberry
from strawberry.types import Info
from app.gql.types import Employer as Employer_gql
from app.db.database import Employer_sql
from app.gql.utils import to_employer_gql
from typing import Optional


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

    @strawberry.mutation
    def update_employer(
        self,
        employer_id: int,
        info: Info,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        contact_email: Optional[int] = None,
    ) -> Employer_gql:
        """
        At least one of title, description, employer_id should be provided.
        Throws error if no employer with the given id has been found.
        """
        # Validate inputs.
        if name is None and industry is None and contact_email is None:
            raise Exception(
                "Please provide at least one employer field you would like to modify."
            )

        db_session = info.context["db_session"]

        # Retrieve the employer object to be updated.
        employer_sql = (
            db_session.query(Employer_sql)
            .filter(Employer_sql.id == employer_id)
            .first()
        )
        if not employer_sql:
            raise Exception("Employer not found")

        if name is not None:
            employer_sql.name = name

        if industry is not None:
            employer_sql.industry = industry

        if contact_email is not None:
            employer_sql.contact_email = contact_email

        db_session.commit()
        db_session.refresh(employer_sql)
        return to_employer_gql(employer_sql, deep=True)

    @strawberry.mutation
    def delete_employer(
        self,
        employer_id: int,
        info: Info,
    ) -> bool:

        db_session = info.context["db_session"]
        employer_sql = (
            db_session.query(Employer_sql)
            .filter(Employer_sql.id == employer_id)
            .first()
        )

        if not employer_sql:
            raise Exception("Employer not found")

        db_session.delete(employer_sql)
        db_session.commit()

        return True
