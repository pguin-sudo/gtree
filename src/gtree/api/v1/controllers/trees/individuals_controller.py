from uuid import UUID

from fastapi import Body, status
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from gtree.api.v1.dependencies import get_current_active_user, get_individual_service
from gtree.api.v1.schemas.trees.individual import (
    IndividualCreateRequestSchema,
    IndividualResponseSchema,
    IndividualUpdateRequestSchema,
)
from gtree.application.services.trees.individual_service import IndividualService
from gtree.domain.entities.user import UserEntity

router = APIRouter(
    tags=["Individuals"],
)


@router.get("/{tree_id}/individuals", response_model=list[IndividualResponseSchema])
async def get_individuals(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: IndividualService = Depends(get_individual_service),
) -> list[IndividualResponseSchema]:
    """Get all individuals for a tree."""
    return [
        IndividualResponseSchema.from_entity(e)
        for e in await service.get_individuals_for_tree(
            user_id=user.id, tree_id=tree_id
        )
    ]


@router.post(
    "/{tree_id}/individuals",
    response_model=IndividualResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_individual(
    tree_id: UUID,
    individual: IndividualCreateRequestSchema = Body(...),
    user: UserEntity = Depends(get_current_active_user),
    service: IndividualService = Depends(get_individual_service),
) -> IndividualResponseSchema:
    """Create a new individual."""
    return IndividualResponseSchema.from_entity(
        await service.create_individual(
            user_id=user.id,
            tree_id=tree_id,
            individual_schema=individual,
        )
    )


@router.get(
    "/{tree_id}/individuals/{individual_id}", response_model=IndividualResponseSchema
)
async def get_individual(
    tree_id: UUID,
    individual_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: IndividualService = Depends(get_individual_service),
) -> IndividualResponseSchema:
    """Get an individual by ID."""
    return IndividualResponseSchema.from_entity(
        await service.get_individual_by_id(
            user_id=user.id,
            tree_id=tree_id,
            individual_id=individual_id,
        )
    )


@router.patch(
    "/{tree_id}/individuals/{individual_id}",
    response_model=IndividualResponseSchema,
)
async def update_individual(
    tree_id: UUID,
    individual_id: UUID,
    individual_schema: IndividualUpdateRequestSchema = Body(...),
    user: UserEntity = Depends(get_current_active_user),
    service: IndividualService = Depends(get_individual_service),
) -> IndividualResponseSchema:
    """Get an individual by ID."""
    return IndividualResponseSchema.from_entity(
        await service.update_individual(
            user_id=user.id,
            tree_id=tree_id,
            individual_id=individual_id,
            individual_schema=individual_schema,
        )
    )


@router.delete(
    "/{tree_id}/individuals/{individual_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_individual(
    tree_id: UUID,
    individual_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: IndividualService = Depends(get_individual_service),
) -> None:
    """Get an individual by ID."""
    await service.delete_individual(
        user_id=user.id,
        tree_id=tree_id,
        individual_id=individual_id,
    )
