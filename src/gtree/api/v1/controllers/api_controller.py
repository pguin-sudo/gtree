from fastapi import APIRouter

router = APIRouter(tags=["API"])


@router.get("/")
def health():
    return {"status": "up"}
