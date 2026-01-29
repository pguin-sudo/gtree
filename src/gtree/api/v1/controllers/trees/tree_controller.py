from uuid import UUID

from fastapi import APIRouter, Depends, status

from gtree.api.v1.dependencies import get_current_active_user, get_tree_service
from gtree.api.v1.schemas.trees.tree import (
    TreeCreateRequestSchema,
    TreeFullResponseSchema,
    TreeResponseSchema,
    TreeUpdateRequestSchema,
)
from gtree.application.services.trees.tree_service import TreeService
from gtree.domain.entities.user import UserEntity

router = APIRouter(
    tags=["Trees"],
)


@router.get("/my", response_model=list[TreeResponseSchema])
async def get_my_trees(
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> list[TreeResponseSchema]:
    """Get all trees accessible by the current user."""
    return [
        TreeResponseSchema.from_entity(e)
        for e in await service.get_accessible_trees(user.id)
    ]


@router.post(
    "/my", response_model=TreeResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_tree(
    create_data: TreeCreateRequestSchema,
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> TreeResponseSchema:
    return TreeResponseSchema.from_entity(
        await service.create_tree(
            owner_id=user.id,
            name=create_data.name,
            description=create_data.description,
        )
    )


@router.get("/{tree_id}", response_model=TreeResponseSchema)
async def get_tree(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> TreeResponseSchema:
    """Get a tree by its ID."""
    return TreeResponseSchema.from_entity(
        await service.get_tree_by_id(user_id=user.id, tree_id=tree_id)
    )


@router.patch("/{tree_id}", response_model=TreeResponseSchema)
async def update_tree(
    tree_id: UUID,
    update_data: TreeUpdateRequestSchema,
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> TreeResponseSchema:
    return TreeResponseSchema.from_entity(
        await service.update_tree(
            tree_id=tree_id,
            user_id=user.id,
            name=update_data.name,
            description=update_data.description,
        )
    )


@router.delete("/{tree_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tree(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> None:
    """Delete a tree (only owner)"""
    await service.delete_tree(tree_id, user.id)


@router.get("/{tree_id}/full", response_model=TreeFullResponseSchema)
async def get_full_tree(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> TreeFullResponseSchema: ...


@router.post("/{tree_id}/share", status_code=status.HTTP_201_CREATED)
async def share_tree_access(
    tree_id: UUID,
    target_user_id: UUID,
    access_level: str = "viewer",
    user: UserEntity = Depends(get_current_active_user),
    service: TreeService = Depends(get_tree_service),
) -> dict[str, str]:
    """Share access to a tree (only owner)"""
    _ = await service.share_access(tree_id, user.id, target_user_id, access_level)
    return {"message": "Access granted"}
