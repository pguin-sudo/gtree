from datetime import date
from typing import override

from sqlalchemy import (
    Date,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gtree.infrastructure.db.models.base import AssociationBaseModel, uuid_pk
from gtree.infrastructure.db.models.trees.individual import IndividualModel


class MarriageModel(AssociationBaseModel):
    __tablename__ = "marriages"

    father_id: Mapped[uuid_pk] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    mother_id: Mapped[uuid_pk] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("individuals.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    marriage_place: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    father: Mapped[IndividualModel] = relationship(
        IndividualModel, foreign_keys=[father_id], back_populates="marriages_as_father"
    )
    mother: Mapped[IndividualModel] = relationship(
        IndividualModel, foreign_keys=[mother_id], back_populates="marriages_as_mother"
    )

    @override
    def __repr__(self) -> str:
        return f"<MarriageModel({self.father_id} — {self.mother_id})>"


IndividualModel.marriages_as_father = relationship(
    MarriageModel,
    foreign_keys=MarriageModel.father_id,
    back_populates="father",
)
IndividualModel.marriages_as_mother = relationship(
    MarriageModel,
    foreign_keys=MarriageModel.mother_id,
    back_populates="mother",
)
