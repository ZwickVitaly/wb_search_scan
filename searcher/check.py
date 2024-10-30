import asyncio

from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


async def check(searched_val, city):
    async with get_async_connection() as client:
        query = f"""
            SELECT rp.query, indexOf(rp.products, {searched_val}) AS product_index, r.quantity
            FROM request_product AS rp
            JOIN Request AS r ON r.query = rp.query
            WHERE has(rp.products, {searched_val}) AND (rp.city = {city})
            ORDER BY product_index;
        """
        res = await client.query(query)
        logger.info(f"{'\n'.join([str((str(date), query, product_index)) for date, query, product_index in res.result_rows])}")


asyncio.run(check(212296429, -1257786))