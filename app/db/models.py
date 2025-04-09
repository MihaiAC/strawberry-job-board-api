# flake8: noqa F401
from __future__ import annotations

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
    class_mapper,
    Session,
)

from sqlalchemy import String, ForeignKey, UniqueConstraint
from typing import List, Dict, Self

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
    def get_all(
        cls: Self,
        db_session: Session,
        selected_fields: str,
        gql: bool = True,
        filter_by_attrs: Dict[str, any] = {},
        ignore_fields: List[str] = [],
        **kwargs,
    ) -> List[Self]:
        """
        cls: Current SQLAlchemy class.
        db_session: Current session object.
        selected_fields: Argument with the same name from the strawberry.Info
        object, cast as string; extracting FKs to join on from it - ideally should have a parser
        do this, but it's out of the scope of this project.
        gql: Whether to cast the returned SQL objects to their equivalent strawberry type
        filter_by_attrs: Attributes to filter on.
        ignore_fields: Again a misnomer, FKs to not join on (has to do with auth).
        """
        query = db_session.query(cls)

        for attr_name, attr_value in filter_by_attrs.items():
            query = query.filter(getattr(cls, attr_name) == attr_value)

        result_objs = query.all()
        return result_objs


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


class Application(Base):
    __tablename__ = "applications"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")

    __table_args__ = (UniqueConstraint("user_id", "job_id", name="unique_user_job"),)
