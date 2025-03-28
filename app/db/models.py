from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
)

from sqlalchemy import (
    String,
    ForeignKey,
)

from typing import List


class Base(DeclarativeBase):
    pass


class Employer(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    contact_email: Mapped[str] = mapped_column(String(254))
    industry: Mapped[str] = mapped_column(String(254))
    jobs: Mapped[List["Job"]] = relationship(
        back_populates="employer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Employer(id={self.id!r}, name={self.name!r}, "
            f"contact_email={self.contact_email!r}, "
            f"industry={self.industry!r})"
        )


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))
    employer: Mapped["Employer"] = relationship(
        "Employer",
        back_populates="jobs",
    )
