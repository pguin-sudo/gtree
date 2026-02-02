from uuid import UUID

from fastapi import Body, status
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from gtree.api.v1.dependencies import (
    get_blood_relation_service,
    get_current_active_user,
)
from gtree.api.v1.schemas.trees.blood_relation import (
    BloodRelationCreateRequestSchema,
    BloodRelationResponseSchema,
)
from gtree.application.services.trees.blood_relation_service import BloodRelationService
from gtree.domain.entities.user import UserEntity

router = APIRouter(
    tags=["Blood Relations"],
)


@router.get(
    "/{tree_id}/blood_relations", response_model=list[BloodRelationResponseSchema]
)
async def get_blood_relations(
    tree_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: BloodRelationService = Depends(get_blood_relation_service),
) -> list[BloodRelationResponseSchema]:
    """Get all blood_relations for a tree."""
    return [
        BloodRelationResponseSchema.from_entity(e)
        for e in await service.get_blood_relations_for_tree(
            user_id=user.id, tree_id=tree_id
        )
    ]


@router.post(
    "/{tree_id}/blood_relations",
    response_model=BloodRelationResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_blood_relation(
    tree_id: UUID,
    blood_relation: BloodRelationCreateRequestSchema = Body(...),
    user: UserEntity = Depends(get_current_active_user),
    service: BloodRelationService = Depends(get_blood_relation_service),
) -> BloodRelationResponseSchema:
    """Create a new blood_relation."""
    return BloodRelationResponseSchema.from_entity(
        await service.create_blood_relation(
            user_id=user.id,
            tree_id=tree_id,
            blood_relation_schema=blood_relation,
        )
    )


@router.get(
    "/{tree_id}/blood_relations/{parent_id}/{child_id}",
    response_model=BloodRelationResponseSchema,
)
async def get_blood_relation(
    tree_id: UUID,
    parent_id: UUID,
    child_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: BloodRelationService = Depends(get_blood_relation_service),
) -> BloodRelationResponseSchema:
    """Get an blood_relation by ID."""
    return BloodRelationResponseSchema.from_entity(
        await service.get_blood_relation_by_id(
            user_id=user.id,
            tree_id=tree_id,
            parent_id=parent_id,
            child_id=child_id,
        )
    )


@router.delete(
    "/{tree_id}/blood_relations/{parent_id}/{child_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_blood_relation(
    tree_id: UUID,
    parent_id: UUID,
    child_id: UUID,
    user: UserEntity = Depends(get_current_active_user),
    service: BloodRelationService = Depends(get_blood_relation_service),
) -> None:
    """Get an blood_relation by ID."""
    await service.delete_blood_relation(
        user_id=user.id,
        tree_id=tree_id,
        parent_id=parent_id,
        child_id=child_id,
    )
