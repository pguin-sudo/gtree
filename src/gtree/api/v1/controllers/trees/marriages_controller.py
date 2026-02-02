from uuid import UUID

from fastapi import Body, status
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from gtree.api.v1.dependencies import (
    get_current_active_user,
    get_marriage_service,
)
from gtree.api.v1.schemas.trees.marriage import (
    MarriageCreateRequestSchema,
    MarriageResponseSchema,
    MarriageUpdateRequestSchema,
)
from gtree.application.services.trees.marriage_service import MarriageService
from gtree.domain.entities.user import UserEntity

router = APIRouter(
    tags=["Blood Relations"],
)


@router.get("/{tree_id}/marriages", response_model=list[MarriageResponseSchema])
async def get_marriages(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: MarriageService = Depends(get_marriage_service),
) -> list[MarriageResponseSchema]:
    """Get all marriages for a tree."""
    return [
        MarriageResponseSchema.from_entity(e)
        for e in await service.get_marriages_for_tree(user_id=user.id, tree_id=tree_id)
    ]


@router.post(
    "/{tree_id}/marriages",
    response_model=MarriageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_marriage(
    tree_id: UUID,
    marriage: MarriageCreateRequestSchema = Body(...),
    user: UserEntity = Depends(get_current_active_user),
    service: MarriageService = Depends(get_marriage_service),
) -> MarriageResponseSchema:
    """Create a new marriage."""
    return MarriageResponseSchema.from_entity(
        await service.create_marriage(
            user_id=user.id,
            tree_id=tree_id,
            marriage_schema=marriage,
        )
    )


@router.get(
    "/{tree_id}/marriages/{father_id}/{mother_id}",
    response_model=MarriageResponseSchema,
)
async def get_marriage(
    tree_id: UUID,
    father_id: UUID,
    mother_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: MarriageService = Depends(get_marriage_service),
) -> MarriageResponseSchema:
    """Get an marriage by ID."""
    return MarriageResponseSchema.from_entity(
        await service.get_marriage_by_id(
            user_id=user.id,
            tree_id=tree_id,
            father_id=father_id,
            mother_id=mother_id,
        )
    )


@router.patch(
    "/{tree_id}/marriages/{father_id}/{mother_id}",
    response_model=MarriageResponseSchema,
)
async def update_marriage(
    tree_id: UUID,
    father_id: UUID,
    mother_id: UUID,
    marriage_schema: MarriageUpdateRequestSchema = Body(...),
    user: UserEntity = Depends(get_current_active_user),
    service: MarriageService = Depends(get_marriage_service),
) -> MarriageResponseSchema:
    """Get an marriage by ID."""
    return MarriageResponseSchema.from_entity(
        await service.update_marriage(
            user_id=user.id,
            tree_id=tree_id,
            father_id=father_id,
            mother_id=mother_id,
            marriage_schema=marriage_schema,
        )
    )


@router.delete(
    "/{tree_id}/marriages/{father_id}/{mother_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_marriage(
    tree_id: UUID,
    father_id: UUID,
    mother_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: MarriageService = Depends(get_marriage_service),
) -> None:
    """Get an marriage by ID."""
    await service.delete_marriage(
        user_id=user.id,
        tree_id=tree_id,
        father_id=father_id,
        mother_id=mother_id,
    )
