from uuid import UUID

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

    async def get_tree_by_id(self, tree_id: UUID, user_id: UUID) -> TreeEntity: ...

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

    async def update_tree(
        self,
        tree_id: UUID,
        user_id: UUID,
        name: str | None = None,
        description: str | None = None,
    ) -> TreeEntity: ...

    async def delete_tree(self, tree_id: UUID, user_id: UUID) -> None: ...

    async def share_access(
        self,
        tree_id: UUID,
        owner_id: UUID,
        target_user_id: UUID,
        access_level: str,
    ) -> None: ...
