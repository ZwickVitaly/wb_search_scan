import asyncio

from sqlalchemy import delete

from db import RequestProduct
from db.base import async_session_maker


async def check():
    async with async_session_maker() as session:
        await session.execute(delete(RequestProduct))
        await session.commit()


asyncio.run(check())