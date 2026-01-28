from datetime import date
from typing import override
import uuid

from sqlalchemy import Date, Enum, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gtree.infrastructure.db.models.base import ObjectBaseModel
from gtree.infrastructure.db.models.trees.tree import TreeModel


class IndividualModel(ObjectBaseModel):
    __tablename__ = "individuals"

    tree_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trees.id", ondelete="CASCADE"), nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    patronymic: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(
        Enum("male", "female", "other", name="gender_types"), nullable=False
    )

    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    birth_date_precision: Mapped[str | None] = mapped_column(String(10), nullable=True)
    death_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    death_date_precision: Mapped[str | None] = mapped_column(String(10), nullable=True)

    birth_place: Mapped[str | None] = mapped_column(Text, nullable=True)
    death_place: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)

    tree: Mapped[TreeModel] = relationship(TreeModel, back_populates="individuals")

    @override
    def __repr__(self) -> str:
        return f"<IndividualModel(id={self.id}, name='{self.first_name} {self.last_name or ''}')>"

    __table_args__ = (
        Index(
            "ix_individuals_tree_name",
            "tree_id",
            func.lower(first_name),
            func.lower(last_name),
            unique=False,
        ),
    )


TreeModel.individuals = relationship(
    IndividualModel,
    back_populates="tree",
    cascade="all, delete-orphan",
    passive_deletes=True,
)
