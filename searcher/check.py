import json

from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check():
    prev = 0
    for i in range(0, 4000000, 10000):
        id_set = set()
        async with async_session_maker() as session:
            res = await session.execute(select(RequestProduct).offset(prev).limit(i))
            res = res.scalars()
            for r in res:
                id_set.update(r.products)
            with open("products.bson", "ab+") as file:
                json.dump(list(id_set), file, indent=2, ensure_ascii=False)

asyncio.run(check())