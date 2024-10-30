from clickhouse_db.get_async_connection import get_async_connection


async def check(searched_val, city):
    async with get_async_connection() as client:
        query = f"""SELECT
                rp.date,
                rp.query,
                r.quantity,
                indexOf(rp.products, {searched_val}) AS product_index
            FROM
                request_product AS rp
            JOIN
                request AS r ON r.query = rp.query
            WHERE
                has(rp.products, {searched_val})
            AND
                (rp.city = {city})
            ORDER BY
            r.quantity DESC;"""
        res = await client.query(query)
