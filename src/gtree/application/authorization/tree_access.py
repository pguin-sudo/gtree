from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

from gtree.application.exceptions.auth import PermissionDeniedException
from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel


def access_to_tree(
    tree_access_level: TreeAccessLevel,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Decorator to check if the user has access to the tree

    Note: Wrapped function must always have self (with `tree_access_repository`) as first argument and tree_id, user_id as keyword arguments
    """

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        async def wrapper(
            self: Any,
            *args: Any,
            tree_id: UUID,
            user_id: UUID,
            **kwargs: Any,
        ) -> Any:
            if await self.tree_access_repository.has_access_to_tree(
                tree_id, user_id, tree_access_level
            ):
                return await func(self, tree_id, user_id, *args, **kwargs)
            raise PermissionDeniedException("User does not have access to the tree")

        return wrapper

    return decorator
