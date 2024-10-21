from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker
from settings import logger


async def check():
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct).filter(RequestProduct.products.contains([63730820])))
        result = rqs.scalars()
    for r in result:
        print(r.query, r.date, r.city)
        rqs = await session.execute(select(Request).filter(Request.query == "вечная спичка огниво"))
        result = rqs.scalars()
        for r in result:
            print(r.query)

asyncio.run(check())