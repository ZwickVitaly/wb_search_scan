import json

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array_agg
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check(wb_id):
    async with async_session_maker() as session:
        result = await session.execute(select(RequestProduct).filter(RequestProduct.products.contains([wb_id])))
        scal = result.scalars()
    for s in scal:
        logger.info(s.query, s.products.index(wb_id))


asyncio.run(check(76280452))