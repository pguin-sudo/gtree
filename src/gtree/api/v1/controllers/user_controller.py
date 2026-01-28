from fastapi import APIRouter, Depends

from gtree.api.v1.dependencies import get_current_active_user
from gtree.api.v1.schemas.user import UserResponseSchema
from gtree.domain.entities.user import UserEntity

router = APIRouter(tags=["User"])


@router.get("/me")
async def auth_user_check_self_info(
    user: UserEntity = Depends(get_current_active_user),
) -> UserResponseSchema:
    """Get the current user's information"""
    return UserResponseSchema.from_entity(user)
