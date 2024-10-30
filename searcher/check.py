import asyncio

from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


async def check(searched_val):
    async with get_async_connection() as client:
        query = f"SELECT query, arrayPosition(products, {searched_val}) AS product_index FROM request_product WHERE has(products, {searched_val}) AND city = -1257786;"
        res = await client.query(query)
        logger.info(res.result_rows)


asyncio.run(check(212296429))