import strawberry
from strawberry.types import Info
from app.db.models import Employer as Employer_sql
from app.gql.types import Employer_gql
from app.db.repositories.employer_repository import EmployerRepository
from typing import Optional
from app.errors.custom_errors import ResourceNotFound
from app.auth.roles import Role
from app.auth.auth_utils import require_role
from graphql import GraphQLError
from app.errors.error_messages import EMPLOYER_ALREADY_EXISTS


@strawberry.type
class EmployerMutation:
    @strawberry.mutation
    @require_role([Role.ADMIN])
    def add_employer(
        self,
        name: str,
        contact_email: str,
        industry: str,
        info: Info,
    ) -> Employer_gql:
        db_session = info.context["db_session"]

        # Enforce email uniqueness.
        existing_employer = EmployerRepository.get_employer_by_email(
            db_session=db_session, selected_fields="", email=contact_email, gql=True
        )
        if existing_employer is not None:
            raise GraphQLError(EMPLOYER_ALREADY_EXISTS)

        employer_sql = Employer_sql(
            name=name, contact_email=contact_email, industry=industry
        )
        db_session.add(employer_sql)
        db_session.commit()
        db_session.refresh(employer_sql)

        return employer_sql.to_gql()

    @strawberry.mutation
    @require_role([Role.ADMIN])
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
    @require_role([Role.ADMIN])
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
