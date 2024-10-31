from dns.e164 import query

from clickhouse_db.get_async_connection import get_async_connection


async def get_keywords_db_data(products, city=-1257786):
    async with get_async_connection() as client:
        query = f"""SELECT rp.query, r.quantity
        FROM request_product AS rp
        JOIN (SELECT * FROM request FINAL) AS r ON r.query = rp.query
        WHERE rp.city = {city} AND arrayExists(x -> x IN {products}, rp.products)
        ORDER BY r.quantity DESC;"""
        query_result = await client.query(query)
        return query_result.result_rows


async def get_product_query_payload(product_id):
    query_result = await get_keywords_db_data(product_id)
    payload = {
        row[0]: row[1]
        for row in query_result
    }
    return payload