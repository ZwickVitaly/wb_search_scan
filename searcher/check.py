import asyncio

from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


async def check():
    async with get_async_connection() as client:
        query = "SELECT * FROM request_product WHERE has(products, 213950484);"
        res = await client.query(query)
        logger.info(res.result_rows)


asyncio.run(check())