from __future__ import annotations

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
)

from sqlalchemy import String, ForeignKey, UniqueConstraint


from typing import List


class Base(DeclarativeBase):
    pass


class Employer(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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


# TODO: Check cascade delete when employer is deleted.
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(254))

    # Plaintext for now.
    password: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String[20])
    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# TODO: Need to test what happens when trying to add existing
# user-job application.
# TODO: Test cascade deletes.
class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["Job"] = relationship("Job", back_populates="applications")

    __table_args__ = (UniqueConstraint("user_id", "job_id", name="unique_user_job"),)
