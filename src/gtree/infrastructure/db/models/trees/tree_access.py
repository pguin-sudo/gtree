from typing import override

from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gtree.infrastructure.db.models.base import AssociationBaseModel, uuid_pk
from gtree.infrastructure.db.models.trees.tree import TreeModel
from gtree.infrastructure.db.models.user import UserModel


class TreeAccessModel(AssociationBaseModel):
    __tablename__ = "tree_access"

    tree_id: Mapped[uuid_pk] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trees.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid_pk] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    tree: Mapped[TreeModel] = relationship(
        TreeModel, foreign_keys=[tree_id], back_populates="users_with_access"
    )
    user: Mapped[UserModel] = relationship(
        UserModel, foreign_keys=[user_id], back_populates="accessible_trees"
    )

    access_level: Mapped[str] = mapped_column(
        Enum("nothing", "viewer", "editor", "owner", name="tree_access_levels"),
        nullable=False,
    )

    @override
    def __repr__(self) -> str:
        return f"<TreeAccessModel({self.tree_id} — {self.user_id})>"


TreeModel.users_with_access = relationship(TreeAccessModel, back_populates="tree")
UserModel.accessible_trees = relationship(TreeAccessModel, back_populates="user")
