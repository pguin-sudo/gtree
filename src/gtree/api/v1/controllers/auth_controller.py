from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from gtree.api.v1.dependencies import get_user_service
from gtree.api.v1.schemas.user import TokenSchema
from gtree.application.services.user_service import UserService

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Create access and refresh tokens for user",
    # responses={...},
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> TokenSchema:
    return TokenSchema.from_entity(
        await user_service.login(form_data.username, form_data.password)
    )


@router.post(
    "/register",
    summary="Register a new user and create access and refresh tokens",
    response_model=TokenSchema,
    # responses={...},
)
async def register(
    form_data: OAuth2PasswordRequestForm = Depends(),
    email: str = Form(...),
    user_service: UserService = Depends(get_user_service),
) -> TokenSchema:
    return TokenSchema.from_entity(
        await user_service.register(form_data.username, form_data.password, email)
    )
