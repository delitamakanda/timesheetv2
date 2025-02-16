from fastapi import APIRouter

from app.schemas.extras.health import HealthCheckResponse
from core.config import config

health_router = APIRouter()


@health_router.get("/")
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(version=config.RELEASE_VERSION, status="OK")
