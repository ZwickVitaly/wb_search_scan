import json

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array_agg
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        subquery = (
            select(func.unnest(RequestProduct.values).label('value'))
            .distinct()
            .subquery()
        )

        # Запрос для подсчета уникальных значений
        result = await session.execute(select(func.count(subquery.c.value)))
        unique_count = result.scalar()
    logger.info(unique_count)


asyncio.run(check())