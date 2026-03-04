from fastapi import APIRouter

from routes.healthy import router as healthy_router

router = APIRouter()
router.include_router(healthy_router)
