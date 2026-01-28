from typing import override

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from gtree.infrastructure.db.models.base import ObjectBaseModel


class TreeModel(ObjectBaseModel):
    __tablename__ = "trees"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    @override
    def __repr__(self) -> str:
        return f"<TreeModel(id={self.id}, name='{self.name}')>"
