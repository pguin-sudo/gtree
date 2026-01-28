from __future__ import annotations

from typing import override

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gtree.infrastructure.db.models.base import AssociationBaseModel, uuid_pk
from gtree.infrastructure.db.models.trees.individual import IndividualModel


class BloodRelationModel(AssociationBaseModel):
    __tablename__ = "blood_relations"

    parent_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("individuals.id", ondelete="CASCADE")
    )
    child_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("individuals.id", ondelete="CASCADE")
    )

    parent: Mapped[IndividualModel] = relationship(
        IndividualModel, foreign_keys=[parent_id], back_populates="child_relations"
    )
    child: Mapped[IndividualModel] = relationship(
        IndividualModel, foreign_keys=[child_id], back_populates="parent_relations"
    )

    __table_args__ = (
        PrimaryKeyConstraint("parent_id", "child_id", name="pk_blood_relation"),
        CheckConstraint("parent_id != child_id", name="no_self_parent"),
        UniqueConstraint("parent_id", "child_id", name="unique_parent_child"),
    )

    @override
    def __repr__(self) -> str:
        return f"<BloodRelationModel(parent={self.parent_id}, child={self.child_id})>"


IndividualModel.parent_relations = relationship(
    BloodRelationModel,
    foreign_keys=BloodRelationModel.child_id,
    back_populates="child",
    cascade="all, delete-orphan",
)
IndividualModel.child_relations = relationship(
    BloodRelationModel,
    foreign_keys=BloodRelationModel.parent_id,
    back_populates="parent",
    cascade="all, delete-orphan",
)
