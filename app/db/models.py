# flake8: noqa F401
from __future__ import annotations

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
    class_mapper,
    Query,
    joinedload,
)

from app.gql.types import (
    Employer_gql,
    Job_gql,
    User_gql,
    Application_gql,
    Base_gql,
)

from strawberry.types import Info

from sqlalchemy import String, ForeignKey, UniqueConstraint
from typing import List, Tuple, Union, Dict

SQL_CLASS_NAME_TO_CLASS = {"Employer"}


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @classmethod
    def get_fk_field_names(cls) -> List[str]:
        """
        Returns the names of the fields corresponding to foreign keys.
        """
        try:
            return [rel.key for rel in class_mapper(cls).relationships]
        except Exception:
            return []

    @classmethod
    def apply_joins(
        cls, query: Query, selected_fields: str
    ) -> Tuple[Query, Dict[str, bool]]:
        """
        Naively decides what joinedloads to do.
        Works only because nested depth is limited to 1.
        To extend this, need to properly parse query from the Info object.
        """
        additional_args = {}
        for field_name in cls.get_fk_field_names():
            if field_name in selected_fields:
                query = query.options(joinedload(getattr(cls, field_name)))
                additional_args[field_name] = True
        return query, additional_args

    @classmethod
    def fetch_and_transform_to_gql(
        cls, info: Info, id: int = None, **kwargs
    ) -> Union[Base_gql, List[Base_gql]]:
        db_session = info.context["db_session"]
        query = db_session.query(cls)

        selected_fields = str(info.selected_fields)

        if id:
            query = query.filter_by(id=id)

        query, additional_args = cls.apply_joins(query, selected_fields)

        if id:
            cls_obj = query.first()
            return cls_obj.to_gql(**additional_args)
        else:
            cls_objs = query.all()
            return [cls_obj.to_gql(**additional_args) for cls_obj in cls_objs]

    def convert_class_name_to_gql_type_name(self) -> str:
        return f"{self.__class__.__name__}_gql"

    def to_gql(self, **kwargs) -> Base_gql:
        """
        kwargs expects a dictionary in the format {
            relationship_key_as_string: bool -> True if the object(s) corresponding
            to this key should be loaded
        }
        """
        gql_class_name = self.convert_class_name_to_gql_type_name()
        gql_class = globals().get(gql_class_name)

        if not gql_class:
            raise ValueError(f"Strawberry type {gql_class_name} not found.")

        # TODO: Need to improve password handling.
        gql_class_init_args = {
            field: getattr(self, field)
            for field in self.__table__.columns.keys()
            if field != "password_hash"
        }

        # Handle nested objects.
        for fk_field in self.get_fk_field_names():
            if kwargs.get(fk_field, False):
                nested_sql_obj = getattr(self, fk_field)
                if isinstance(nested_sql_obj, list):
                    gql_class_init_args[fk_field] = [
                        obj.to_gql() for obj in nested_sql_obj
                    ]
                else:
                    gql_class_init_args[fk_field] = (
                        nested_sql_obj.to_gql() if nested_sql_obj else None
                    )
            else:
                gql_class_init_args[fk_field] = None

        gql_obj = gql_class(**gql_class_init_args)
        return gql_obj


class Employer(Base):
    __tablename__ = "employers"

    name: Mapped[str] = mapped_column(String(40))
    contact_email: Mapped[str] = mapped_column(String(254))
    industry: Mapped[str] = mapped_column(String(254))
    jobs: Mapped[List["Job"]] = relationship(
        back_populates="employer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Employer(id={self.id!r}, name={self.name!r}, "
            f"contact_email={self.contact_email!r}, "
            f"industry={self.industry!r})"
        )


class Job(Base):
    __tablename__ = "jobs"
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))
    employer_id: Mapped[int] = mapped_column(
        ForeignKey("employers.id", ondelete="CASCADE")
    )
    employer: Mapped["Employer"] = relationship(
        "Employer",
        back_populates="jobs",
    )
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Job(id={self.id!r}, title={self.title!r}, "
            f"description={self.description[:30]!r}..., "
            f"employer_id={self.employer_id!r})"
        )


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(254))

    # Plaintext for now.
    password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String[20])
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# TODO: Need to test what happens when trying to add existing
# user-job application.
class Application(Base):
    __tablename__ = "applications"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")

    __table_args__ = (UniqueConstraint("user_id", "job_id", name="unique_user_job"),)
