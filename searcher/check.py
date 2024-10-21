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
    moscow = dict()
    krasnodar = dict()
    ekat = dict()
    vlad = dict()
    for r in result:
        for p, i in zip(r.products, r.positions):
            if p == wb_id:
                if r.city == 1:
                    moscow[r.query] = i
                elif r.city == 2:
                    krasnodar[r.query] = i
                elif r.city == 3:
                    ekat[r.query] = i
                elif r.city == 4:
                    vlad[r.query] = i
    res = [{"Москва":moscow}, {"Краснодар":krasnodar}, {"Екатеринбург":ekat}, {"Владивосток":vlad}]
    print(json.dumps(res, indent=2, ensure_ascii=False))


asyncio.run(check(181082581))