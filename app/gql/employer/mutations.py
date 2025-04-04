import strawberry
from strawberry.types import Info
from app.db.models import Employer as Employer_sql, Employer_gql
from typing import Optional
from app.errors.custom_errors import ResourceNotFound


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

        return employer_sql.to_gql()

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
        db_session = info.context["db_session"]

        # Retrieve the employer object to be updated.
        employer_sql = (
            db_session.query(Employer_sql)
            .filter(Employer_sql.id == employer_id)
            .first()
        )
        if not employer_sql:
            raise ResourceNotFound("Employer")

        if name is not None:
            employer_sql.name = name

        if industry is not None:
            employer_sql.industry = industry

        if contact_email is not None:
            employer_sql.contact_email = contact_email

        db_session.commit()
        db_session.refresh(employer_sql)
        return employer_sql.to_gql()

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
            raise ResourceNotFound("Employer")

        db_session.delete(employer_sql)
        db_session.commit()

        return True
