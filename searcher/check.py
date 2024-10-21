from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct).order_by(func.cardinality(RequestProduct.products).desc()).limit(10))
        result = rqs.scalars()
    for r in result:
        if len(r.products) < 10:
            logger.info(f"{r.query} - {r.products}")

asyncio.run(check())