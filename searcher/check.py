import asyncio

from clickhouse_connect.driver import AsyncClient

from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


async def check(searched_val, city):
    async with get_async_connection() as client:
        client: AsyncClient = client
        query = f"""SELECT sd.query, groupArray((rp.date, r.quantity, indexOf(rp.products, {searched_val}) AS product_index)) AS date_info
        FROM (SELECT rp.query, rp.date, r.quantity, rp.products 
        FROM request_product AS rp JOIN
        request AS r ON r.query = rp.query 
        WHERE has(rp.products, {searched_val})
        AND (rp.city = {city}) 
        AND (rp.date BETWEEN '2024-10-29' AND '2024-10-31')
        ORDER BY rp.date, r.quantity DESC
        ) AS sd 
        GROUP BY sd.query 
        ORDER BY sd.query;"""
        # query = f"SELECT rp.query, r.quantity FROM request_product as rp JOIN request AS r ON r.query = rp.query WHERE rp.city = {city} AND arrayExists(x -> x IN {searched_val}, rp.products) ORDER BY r.quantity DESC;"
        # query = f"SELECT city, count(*) FROM request_product GROUP BY city;"
        res = await client.query(query)
        # json_result = [{"date": str(row[0]), "products": row[1]} for row in res.result_rows]
        logger.info(res.result_rows)


asyncio.run(check(212296429, -1257786))