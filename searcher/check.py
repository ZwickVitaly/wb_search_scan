from sqlalchemy import select
import asyncio
from db import RequestProduct
from db.base import async_session_maker


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct))
        result = list(rqs.scalars())
    print(len(result))


asyncio.run(check())