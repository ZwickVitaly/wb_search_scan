import asyncio
import json
import time
from datetime import datetime
from multiprocessing import Pool
from aiofiles import open as aiopen
from aiohttp import ClientSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from parser.get_single_query_data import get_query_data
from db.base import async_session_maker
from db import City, Request, RequestProduct, Product
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

async def save_to_db(queue, model, update=False):
    logger.critical("ЕЩЁ")
    while True:
        items = []
        item = None
        while len(items) < 500:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, list):
                items.extend(item)
            else:
                items.append(item)
            queue.task_done()
        if items:
            async with async_session_maker() as session:
                if not update:
                    await session.execute(insert(model).values(items))
                    logger.critical("УСПЕХ 1")
                else:
                    # stmt = insert(model)
                    # excluded_fields = {col.name: stmt.excluded[col.name] for col in model.__table__.columns if
                    #                    not col.primary_key}
                    primary_fields = [col.name for col in model.__table__.columns if col.primary_key]
                    try:
                        await session.execute(
                            insert(model).values(items).on_conflict_do_nothing(
                                index_elements=primary_fields,
                            )
                        )
                    except Exception as e:
                        logger.error(f"{e}")
                    logger.critical("УСПЕХ!")
                await session.commit()
        if item is None:
            await queue.put(item)
            break




async def get_r_data_q(queue: asyncio.Queue, city, date, http_session, product_queue=None, request_product_queue=None):
    while True:
        r = await queue.get()
        if r is None:
            await queue.put(r)
            break
        await get_r_data(r=r, city=city, date=date, http_session=http_session, product_queue=product_queue, request_product_queue=request_product_queue)
        queue.task_done()

async def try_except_query_data(query_string, dest, limit, page, http_session, rqa=5):
    try:
        x = await get_query_data(
            http_session=http_session,
            query_string=query_string,
            dest=dest,
            limit=limit,
            page=page,
            rqa=rqa,
            timeout=10
        )
    except ValueError:
        x = {"products": []}
    return x

async def get_r_data(r, city, date, http_session, product_queue=None, request_product_queue=None):
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
                        rqa=4,
                        http_session=http_session,
                    )
                ) for i in range(1,4)
            ]
            result = await asyncio.gather(*tasks)
            for res in result:
                full_res.extend(res.get("products", []))
            if not full_res:
                full_res = []
            logger.critical("ПОЧТИ")
            # seen = set()
            products = []
            for p in full_res:
                # if p.get("id") not in seen:
                products.append(
                    {
                        "wb_id": p.get("id"),
                        "name": p.get("name"),
                        "brand": p.get("brand"),
                        "brandId": p.get("brandId"),
                        "supplier": p.get("supplier"),
                        "supplierId": p.get("supplierId"),
                        "entity": p.get("entity"),
                    }
                )
                #     seen.add(p.get("id"))
                # seen.clear()
            async with aiopen("dump.bson", "ab") as aiofile:
                for prod in products:
                    await aiofile.write(f"{json.dumps(prod, indent=2, ensure_ascii=False)},".encode())
            logger.critical("ПОЧТИ 2")
            request_product = {
                "city": city.id,
                "query": r.query,
                "products": [p.get("id") for p in full_res],
                "positions": [i for i in range(1, len(full_res) + 1)],
                "natural_positions": [p.get("log", {}).get("position", 0) for p in full_res],
                "date": date
            }
            await request_product_queue.put(request_product)
            return
        except Exception as e:
            logger.critical(f"{e}")
            break

async def get_city_result(city, date):
    requests = [r for r in await get_requests_data() if not r.query.isdigit()]
#     logger.info(f"{city.name} start, {len(requests)}")
    product_queue = asyncio.Queue()
    request_product_queue = asyncio.Queue(10)
    workers_queue = asyncio.Queue(10)
    product_save_task = [asyncio.create_task(save_to_db(product_queue, Product, update=True)) for _ in range(20)]
    request_product_save_task = [asyncio.create_task(save_to_db(request_product_queue, RequestProduct)) for _ in range(10)]
    async with ClientSession() as http_session:
        requests_tasks = [
            asyncio.create_task(
                get_r_data_q(
                    queue=workers_queue,
                    city=city,
                    date=date,
                    http_session=http_session,
                    product_queue=product_queue,
                    request_product_queue=request_product_queue
                )
            ) for _ in range(20)
        ]
        while requests:
            await workers_queue.put(requests.pop())
        await workers_queue.put(None)
        await asyncio.gather(*requests_tasks)
        await product_queue.put(None)
        await request_product_queue.put(None)
        await asyncio.gather(*product_save_task, *request_product_save_task)
#             logger.info(f"{city.name} BATCH {_}")
#     logger.info(f"{city.name} complete")

def run_pool_threads(func, *args, **kwargs):
#     logger.info("Применен процесс")
    asyncio.run(func(*args, **kwargs))

def get_results():
    with open("dump.bson", "wb+") as file:
        file.write(b"[\n")
        pass
    start = time.time()
    logger.info("Вход в программу")
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

