from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(func.count()).select_from(RequestProduct))
        result = rqs.scalar_one()
    logger.info(result)

asyncio.run(check())