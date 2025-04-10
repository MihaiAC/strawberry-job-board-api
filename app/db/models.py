# flake8: noqa F401
from __future__ import annotations

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
    class_mapper,
    Session,
    Query,
)

from sqlalchemy import and_, or_

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
    def apply_single_attr_multivalued_filter(
        cls,
        query: Query,
        attr_name: str,
        attr_values: list,
    ) -> Query:
        query = query.filter(getattr(cls, attr_name).in_(attr_values))
        return query

    @classmethod
    def apply_multi_attr_multivalued_filter(
        cls,
        query: Query,
        attr_names: tuple[str, ...],
        attr_values: list[tuple],
    ) -> Query:
        conditions = []
        for values in attr_values:
            condition_parts = []
            for attr, value in zip(attr_names, values):
                condition_parts.append(getattr(cls, attr) == value)
            conditions.append(and_(*condition_parts))
        return query.filter(or_(*conditions))

    @classmethod
    def apply_multi_attr_singlevalued_filter(
        cls,
        query: Query,
        filter_by_attrs: dict,
    ) -> Query:
        for attr_name, attr_value in filter_by_attrs.items():
            query = query.filter(getattr(cls, attr_name) == attr_value)
        return query

    @classmethod
    def get_all(
        cls: Self,
        db_session: Session,
        filter_by_attrs: dict = {},
    ) -> List[Self]:
        """
        cls: Current SQLAlchemy class.
        db_session: Current session object.
        filter_by_attrs: Attributes to filter on.
        Dictionary, which can be:
        1. Empty (no filtering needed);
        2. In the format {attr_name: attr_val (scalar)};
        Will add a filter for each (attr_name, attr_val) pair.
        3. In the format {attr_name: [attr_val] (list)};
        Must have only one entry. Finds all objects which have an attr_name
        equal to one of the values in the list.
        4. In the format {(attr_name1, attr_name2, ...): [(val1_ii, val2_ii, ...)]}
        Must have only one entry.
        Will find all objects whose values of (attr_name1, attr_name2, ...) match
        one of the tuples in the list.
        """
        query = db_session.query(cls)

        if len(filter_by_attrs) > 0:
            first_attr_key = next(iter(filter_by_attrs))
            if isinstance(filter_by_attrs[first_attr_key], list):
                if len(filter_by_attrs) > 1:
                    raise Exception("filter_by_attrs has incorrect format.")
                if isinstance(first_attr_key, str):
                    # Format 3.
                    attr_name = first_attr_key
                    attr_values = filter_by_attrs[attr_name]
                    query = cls.apply_single_attr_multivalued_filter(
                        query,
                        attr_name,
                        attr_values,
                    )
                else:
                    # Format 4.
                    attr_names = first_attr_key
                    attr_values = filter_by_attrs[attr_names]
                    query = cls.apply_multi_attr_multivalued_filter(
                        query,
                        attr_names,
                        attr_values,
                    )
            else:
                # Format 2.
                query = cls.apply_multi_attr_singlevalued_filter(query, filter_by_attrs)

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
