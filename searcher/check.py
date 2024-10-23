import json

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array_agg
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        res = await session.execute(select(func.sum(func.array_length(RequestProduct.products, 1))))
        res = res.scalar()
    logger.info(res)


asyncio.run(check())