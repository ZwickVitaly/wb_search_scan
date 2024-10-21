import json

from sqlalchemy import select, func
import asyncio
from db import RequestProduct, Request
from db.base import async_session_maker
from settings import logger


async def check(wb_id):
    async with async_session_maker() as session:
        rqs = await session.execute(select(RequestProduct).filter(RequestProduct.products.contains([wb_id])))
        result = rqs.scalars()
    moscow = set()
    krasnodar = set()
    ekat = set()
    vlad = set()
    for r in result:
        for p, i in zip(r.products, r.positions):
            if p == wb_id:
                if r.city == 1:
                    moscow.add(r.query)
                elif r.city == 2:
                    krasnodar.add(r.query)
                elif r.city == 3:
                    ekat.add(r.query)
                elif r.city == 4:
                    vlad.add(r.query)
    res = [{"Москва":list(moscow)}, {"Краснодар":list(krasnodar)}, {"Екатеринбург":list(ekat)}, {"Владивосток":list(vlad)}]
    print(json.dumps(res, indent=2, ensure_ascii=False))


asyncio.run(check(181082581))