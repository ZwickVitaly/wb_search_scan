import json

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array_agg
import asyncio
from db import RequestProduct, Request, Product, City
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        result = await session.execute(select(City))
        scal = result.scalars()
    for c in scal:
        print(c.name)
    # for s in scal:
    #     logger.info(f"{s.query}, {s.products.index(wb_id)}")


asyncio.run(check())