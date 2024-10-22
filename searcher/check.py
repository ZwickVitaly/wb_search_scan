import json

from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request, Product
from db.base import async_session_maker
from settings import logger


async def check(wb_id):
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct))
        result = rqs.scalars()
    id_set = set()
    for r in result:
        id_set.update(r.products)
    id_set = list(id_set)
    with open("products.bson", "wb+") as file:
        json.dump(id_set, file, indent=2, ensure_ascii=False)