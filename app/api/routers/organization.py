from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.base import ErrorResponse
from app.api.schemas.organization import OrganizationListResponse, OrganizationResponse
from app.config.db import get_async_session
from app.services.organization import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get(
    "/{organization_id:int}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    name="Получить информацию об организации",
    description="Получить подробную информацию об организации по его идентификатору",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        404: {"model": ErrorResponse, "description": "Организация не найдена"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_organization(
    organization_id: int = Path(..., ge=1, description="Идентификатор организации"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationResponse:
    organization = await OrganizationService(session).get_by_id(organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail=f"Organization not found id={organization_id}")
    return OrganizationResponse.from_entity(organization)


@router.get(
    "/building/{building_id}",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    name="Получить список организаций в здании",
    description="Получить список организаций, находящихся в указанном здании по его идентификатору",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        404: {"model": ErrorResponse, "description": "Здание не найдено"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_by_building(
    building_id: int = Path(..., gt=0, description="Идентификатор здания"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationListResponse:
    organizations = await OrganizationService(session).get_by_building_id(building_id)
    return OrganizationListResponse.from_entities(organizations)


@router.get(
    "/category/{category_id}",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    name="Получить список организаций с деятельностью",
    description="Получить список организаций, относящиеся к указанному виду деятельности по его идентификатору",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        404: {"model": ErrorResponse, "description": "Деятельность не найдена"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_by_category(
    category_id: int = Path(..., gt=0, description="Идентификатор деятельности"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationListResponse:
    organizations = await OrganizationService(session).get_by_category_id(category_id)
    return OrganizationListResponse.from_entities(organizations)


@router.get(
    "/nested-categories/{category_id}",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    name="Получить список организаций с деятельностью и её наследниками",
    description="Получить список организаций, относящиеся к указанному виду деятельности и всех наследников",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        404: {"model": ErrorResponse, "description": "Деятельность не найдена"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_by_nested_categories(
    category_id: int = Path(..., gt=0, description="Идентификатор деятельности"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationListResponse:
    organizations = await OrganizationService(session).get_by_nested_categories(category_id)
    return OrganizationListResponse.from_entities(organizations)


@router.get(
    "/geo/radius",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    name="Получить список организаций в радиусе",
    description="Получить список организаций, находящихся в зданиях в указанном радиусе по долготе, широте и радиусе",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def get_organizations_in_radius(
    latitude: float = Query(..., ge=-90, le=90, description="Широта"),
    longitude: float = Query(..., ge=-180, le=180, description="Долгота"),
    radius_km: float = Query(..., gt=0, le=50, description="Радиус в километрах"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationListResponse:
    organizations = await OrganizationService(session).get_organizations_in_radius(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    return OrganizationListResponse.from_entities(organizations)


@router.get(
    "/search",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    name="Поиск организации по названию",
    description="Получить список организаций по входящим символам в название",
    responses={
        401: {"model": ErrorResponse, "description": "Пользователь не авторизован"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
    },
)
async def search_organizations_by_name(
    name: str = Query(..., min_length=2, description="Часть названия организации"),
    session: AsyncSession = Depends(get_async_session),
) -> OrganizationListResponse:
    organizations = await OrganizationService(session).search_by_name(name)
    return OrganizationListResponse.from_entities(organizations)
