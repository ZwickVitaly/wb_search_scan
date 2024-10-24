import json

from sqlalchemy import select, func, delete
from sqlalchemy.dialects.postgresql import array_agg
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        await session.execute(delete(RequestProduct))
        subquery = (
            select(func.unnest(RequestProduct.products).label('value'))
            .order_by("value")
            .distinct()
            .subquery()
        )

        # Запрос для подсчета уникальных значений
        result = await session.execute(select(func.count(subquery.c.value)))
        unique_count = result.scalar()

        subquery = (
            select(func.unnest(RequestProduct.products).label('value'))
            .where(RequestProduct.city == 1)
            .distinct()
            .subquery()
        )

        # Запрос для подсчета уникальных значений
        result = await session.execute(select(func.count()).select_from(RequestProduct).where(RequestProduct.city == 1))
        reqs = result.scalar()
    logger.info(unique_count // reqs)


asyncio.run(check())