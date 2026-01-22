from fastapi import APIRouter, Depends

from gtree.api.v1.dependencies import get_current_active_user
from gtree.api.v1.schemas.user import UserSchema

router = APIRouter(tags=["User"])


@router.get("/me")
async def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_user),
) -> UserSchema:
    return user
