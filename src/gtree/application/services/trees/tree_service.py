from uuid import UUID

from gtree.application.authorization.tree_access import access_to_tree
from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.tree import TreeEntity
from gtree.domain.entities.trees.tree_access import TreeAccessEntity
from gtree.infrastructure.db.repositories.trees.tree import TreeRepository
from gtree.infrastructure.db.repositories.trees.tree_access import TreeAccessRepository


class TreeService:
    def __init__(
        self,
        tree_repository: TreeRepository,
        tree_access_repository: TreeAccessRepository,
    ):
        self.tree_repository = tree_repository
        self.tree_access_repository = tree_access_repository

    async def get_accessible_trees(self, user_id: UUID) -> list[TreeEntity]:
        return await self.tree_repository.get_accessible_trees(
            user_id, TreeAccessLevel.OWNER
        )

    @access_to_tree(TreeAccessLevel.VIEWER)
    async def get_tree_by_id(self, tree_id: UUID, user_id: UUID) -> TreeEntity:  # noqa: ARG002
        return await self.tree_repository.get_by_id(tree_id)

    async def get_full_tree(self, tree_id: UUID, user_id: UUID) -> TreeEntity: ...

    async def create_tree(
        self, owner_id: UUID, name: str, description: str
    ) -> TreeEntity:
        tree = TreeEntity.create_tree(name, description)
        tree = await self.tree_repository.create(tree)
        tree_access = TreeAccessEntity.create_tree_access(
            owner_id, tree.id, TreeAccessLevel.OWNER
        )
        _ = await self.tree_access_repository.create(tree_access)
        return tree

    @access_to_tree(TreeAccessLevel.OWNER)
    async def update_tree(
        self,
        tree_id: UUID,
        user_id: UUID,  # noqa: ARG002
        name: str | None = None,
        description: str | None = None,
    ) -> TreeEntity:
        tree = await self.tree_repository.get_by_id(tree_id)
        if name is not None:
            tree.name = name
        if description is not None:
            tree.description = description
        await self.tree_repository.update(tree)
        return tree

    @access_to_tree(TreeAccessLevel.OWNER)
    async def delete_tree(self, tree_id: UUID, user_id: UUID) -> None:  # noqa: ARG002
        await self.tree_repository.delete(tree_id)

    @access_to_tree(TreeAccessLevel.OWNER)
    async def share_access(
        self,
        tree_id: UUID,
        user_id: UUID,  # noqa: ARG002
        target_user_id: UUID,
        access_level: str,
    ) -> None:
        tree_access = TreeAccessEntity.create_tree_access(
            target_user_id, tree_id, access_level
        )
        _ = await self.tree_access_repository.upsert(tree_access)
