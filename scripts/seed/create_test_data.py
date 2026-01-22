import asyncio
from random import choice, randint

from sqlalchemy import func

from app.config.db import async_session_maker
from app.infrastructure.db import Building, Category, Organization, Phone


async def main():
    async with async_session_maker() as session:
        buildings = [
            Building(
                address="ул. Тестовая, д.1",
                latitude=54.751244,
                longitude=20.618423,
                location=func.ST_SetSRID(func.ST_MakePoint(20.618423, 54.751244), 4326),
            ),
            Building(
                address="ул. Продовая, д.7",
                latitude=54.752615,
                longitude=20.622615,
                location=func.ST_SetSRID(func.ST_MakePoint(20.622615, 54.752615), 4326),
            ),
            Building(
                address="ул. Стендовая, д.23",
                latitude=54.755423,
                longitude=20.615244,
                location=func.ST_SetSRID(func.ST_MakePoint(20.615244, 54.755423), 4326),
            ),
        ]
        session.add_all(buildings)
        await session.flush()

        eat = Category(name="Еда")
        furniture = Category(name="Мебель")
        session.add_all([eat, furniture])
        await session.flush()

        meat = Category(name="Мясная продукция", base_category_id=eat.id)
        milk = Category(name="Молочная продукция", base_category_id=eat.id)
        bed = Category(name="Кровать", base_category_id=furniture.id)
        session.add_all([meat, milk, bed])
        await session.flush()

        organizations = []
        for i in range(10):
            organization = Organization(name=f"ООО Тестовая организация {i}", building_id=choice(buildings).id)
            cats = [choice([eat, meat, milk, furniture, bed])]
            organization.categories.extend(cats)
            organizations.append(organization)
        session.add_all(organizations)
        await session.flush()

        for organization in organizations:
            phones = []
            for _ in range(randint(1, 3)):
                phones.append(
                    Phone(
                        number=f"+7-999-{randint(100, 999)}-{randint(10, 99)}-{randint(10, 99)}",
                        organization_id=organization.id,
                    )
                )
            session.add_all(phones)
            await session.flush()

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
