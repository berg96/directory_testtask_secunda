from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.base import ErrorResponse
from app.api.schemas.building import BuildingListResponse
from app.config.db import get_async_session
from app.services.building import BuildingService

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get(
    "/geo/radius",
    response_model=BuildingListResponse,
    status_code=status.HTTP_200_OK,
    name="Получить список зданий в радиусе",
    description="Получить список зданий, находящихся в указанном радиусе по долготе, широте и радиусе (км)",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_buildings_in_radius(
    latitude: float = Query(..., ge=-90, le=90, description="Широта"),
    longitude: float = Query(..., ge=-180, le=180, description="Долгота"),
    radius_km: float = Query(..., gt=0, le=50, description="Радиус в километрах"),
    session: AsyncSession = Depends(get_async_session),
) -> BuildingListResponse:
    buildings = await BuildingService(session).get_buildings_in_radius(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    return BuildingListResponse.from_entities(buildings)
