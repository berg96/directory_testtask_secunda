from typing import Optional

import pytest_asyncio
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.settings import settings
from app.infrastructure.db import Building, Category, Organization, Phone

from .fixtures.entities import *  # noqa
from .fixtures.orm_fakes import *  # noqa


@pytest_asyncio.fixture
async def async_engine():
    DATABASE_URL = settings.get_db_url()
    engine = create_async_engine(DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def create_building(async_session):
    async def _create(address: str, latitude: float, longitude: float) -> Building:
        building = Building(
            address=address,
            latitude=latitude,
            longitude=longitude,
            location=func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
        )
        async_session.add(building)
        await async_session.flush()
        return building

    return _create


@pytest_asyncio.fixture
async def create_category(async_session):
    async def _create(name: str, base_category_id: Optional[int] = None) -> Category:
        category = Category(name=name)
        if base_category_id:
            category.base_category_id = base_category_id
        async_session.add(category)
        await async_session.flush()
        return category

    return _create


@pytest_asyncio.fixture
async def create_organization(async_session, create_building, create_category):
    async def _create(
        name: str,
        building_id: Optional[int] = None,
        category_ids: Optional[list[int]] = None,
    ) -> Organization:
        organization = Organization(name=name)
        if building_id:
            organization.building_id = building_id
        if category_ids:
            for category_id in category_ids:
                category = await async_session.get(Category, category_id)
                if category:
                    organization.categories.append(category)

        async_session.add(organization)
        await async_session.flush()
        return organization

    return _create


@pytest_asyncio.fixture
async def create_phone(async_session):
    async def _create(number: str, organization_id: int):
        phone = Phone(number=number, organization_id=organization_id)
        async_session.add(phone)
        await async_session.flush()
        return phone

    return _create
