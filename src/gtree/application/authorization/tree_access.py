from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any
from uuid import UUID

from gtree.application.exceptions.auth import PermissionDeniedException
from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel

if TYPE_CHECKING:
    from gtree.infrastructure.db.repositories.trees.tree_access import (
        TreeAccessRepository,
    )


def access_to_tree(
    tree_access_level: TreeAccessLevel,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator to check if the user has access to the tree

    Note: Wrapped function must always have self (with attribute `tree_access_repository`)
    as first argument and user_id, tree_id as keyword arguments
    """

    def decorator(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        async def wrapper(
            self: Any,
            *args: Any,
            user_id: UUID,
            tree_id: UUID,
            **kwargs: Any,
        ) -> Any:
            repo: TreeAccessRepository = self.tree_access_repository
            if await repo.has_minimum_access_level(
                user_id=user_id, tree_id=tree_id, min_access_level=tree_access_level
            ):
                return await func(
                    self, *args, user_id=user_id, tree_id=tree_id, **kwargs
                )
            raise PermissionDeniedException("User does not have access to the tree")

        return wrapper

    return decorator
