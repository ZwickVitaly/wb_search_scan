import asyncio
from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


async def check(searched_val, city):
    async with get_async_connection() as client:
        # query = f"""SELECT
        #         rp.date,
        #         rp.query,
        #         r.quantity,
        #         indexOf(rp.products, {searched_val}) AS product_index
        #     FROM
        #         request_product AS rp
        #     JOIN
        #         request AS r ON r.query = rp.query
        #     WHERE
        #         has(rp.products, {searched_val})
        #     AND
        #         (rp.city = {city})
        #     ORDER BY
        #     r.quantity DESC;"""
        query = f"SELECT query FROM request_product WHERE city = {city} AND arrayExists(x -> x IN {searched_val}, products) ORDER BY query;"
        res = await client.query(query)
        logger.info(res.result_rows)


asyncio.run(check((212296429, 238552341, 196119668), -1257786))