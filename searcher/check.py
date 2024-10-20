from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct))
        result = rqs.scalars()
    for r in result:
        logger.info(r.query)

asyncio.run(check())