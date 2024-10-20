import asyncio
import time
from datetime import datetime
from multiprocessing import Pool

from aiohttp import ClientSession
from sqlalchemy import select

from parser.get_single_query_data import get_query_data
from db.base import async_session_maker
from db import City, Request, RequestProduct
from settings import logger



async def get_cities_data():
    async with async_session_maker() as s:
        q = await s.execute(select(City))
        cities = q.scalars()
    return cities

async def get_requests_data():
    async with async_session_maker() as s:
        q = await s.execute(select(Request).order_by(Request.quantity.desc()).limit(1000))
        requests = q.scalars()
    return requests

# async def save_to_db(queue):
#     while True:
#         items = []
#         item = None
#         while len(items) < 1000:
#             item = await queue.get()
#             if item is None:
#                 break
#             items.append(item)
#         if items:
#             async with async_session_maker() as session:
#                 session.add_all(items)
#                 await session.commit()
#         if item is None:
#             break

async def try_except_query_data(query_string, dest, limit, page, http_session, rqa=3):
    try:
        x = await get_query_data(
            http_session=http_session,
            query_string=query_string,
            dest=dest,
            limit=limit,
            page=page,
            rqa=rqa,
            timeout=3
        )
    except ValueError:
        x = {"products": []}
    return x

async def get_r_data(r, city, date, http_session):
    while True:
        try:
            full_res = []
            tasks = [
                asyncio.create_task(
                    try_except_query_data(
                        query_string=r.query,
                        dest=city.dest,
                        limit=300,
                        page=i,
                        rqa=3,
                        http_session=http_session,
                    )
                ) for i in range(1,4)
            ]
            result = await asyncio.gather(*tasks)
            for res in result:
                full_res.extend(res.get("products", []))
            if not full_res:
                full_res = []
            request_product = RequestProduct(
                city=city.id,
                query=r.query,
                products=[p.get("id") for p in full_res],
                positions=[i for i in range(1, len(full_res) + 1)],
                natural_positions=[p.get("log", {}).get("position", 0) for p in full_res],
                date=date
            )
            return request_product
        except Exception as e:
#             logger.critical(f"{e}")
            break

async def get_city_result(city, date):
    requests = [r for r in await get_requests_data() if not r.query.isdigit()]
#     logger.info(f"{city.name} start, {len(requests)}")
    prev = 0
    async with ClientSession() as http_session:
        for _ in range(100, len(requests) + 100, 100):
#             logger.critical(f"ЧТО ЗА ФИГНЯ {prev} - {_}")
            tasks = [asyncio.create_task(get_r_data(r=r, city=city, date=date, http_session=http_session)) for r in requests[prev:_]]
#             logger.info(len(tasks))
            rp = await asyncio.gather(*tasks)
            prev = _
#             logger.critical(len(rp))
            async with async_session_maker() as session:
                session.add_all(rp)
                await session.commit()
#             logger.info(f"{city.name} BATCH {_}")
#     logger.info(f"{city.name} complete")

def run_pool_threads(func, *args, **kwargs):
#     logger.info("Применен процесс")
    asyncio.run(func(*args, **kwargs))

def get_results():
    start = time.time()
#     logger.info("Вход в программу")
    today = datetime.now().date()
    loop = asyncio.new_event_loop()
    cities = loop.run_until_complete(get_cities_data())
#     logger.info("Города есть")
    cities = list(cities)
#     logger.info("Начало обхода")
    with Pool(len(cities)) as p:
        tasks = [
            p.apply_async(run_pool_threads, args=[get_city_result, city, today])
            for city in cities
        ]
        p.close()
        p.join()
    end = time.time()
    logger.info(f"END TIME: {round(end - start, 2)}s")

get_results()

