from fastapi import APIRouter

from gtree.api.v1.controllers.api_controller import (
    router as api_router,
)
from gtree.api.v1.controllers.auth_controller import (
    router as auth_router,
)
from gtree.api.v1.controllers.trees.individuals_controller import (
    router as individuals_router,
)
from gtree.api.v1.controllers.trees.trees_controller import (
    router as trees_router,
)
from gtree.api.v1.controllers.users_controller import (
    router as users_router,
)

api_v1_router = APIRouter()
api_v1_router.include_router(api_router, prefix="")
api_v1_router.include_router(auth_router, prefix="/auth")
api_v1_router.include_router(trees_router, prefix="/trees")
api_v1_router.include_router(individuals_router, prefix="/trees")
api_v1_router.include_router(users_router, prefix="/users")
