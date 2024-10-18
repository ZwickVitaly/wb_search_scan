from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(func.count()).select_from(RequestProduct))
        result = rqs.scalars()
    for i in result:
        print(i)
    # print(len([r.query for r in result if r.query.isdigit()]))


asyncio.run(check())