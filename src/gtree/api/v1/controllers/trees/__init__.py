from fastapi.routing import APIRouter

from gtree.api.v1.controllers.trees.blood_relations_controller import (
    router as blood_relations_router,
)
from gtree.api.v1.controllers.trees.individuals_controller import (
    router as individuals_router,
)
from gtree.api.v1.controllers.trees.marriages_controller import (
    router as marriages_router,
)
from gtree.api.v1.controllers.trees.trees_controller import (
    router as trees_router,
)

router = APIRouter()


router.include_router(blood_relations_router, prefix="")
router.include_router(individuals_router, prefix="")
router.include_router(marriages_router, prefix="")
router.include_router(trees_router, prefix="")
