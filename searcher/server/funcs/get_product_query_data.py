from clickhouse_db.get_async_connection import get_async_connection
from datetime import date


async def get_db_data(product_id, dates_list, city):
    max_date: date = max(dates_list)
    min_date: date = min(dates_list)
    async with get_async_connection() as client:
        query = f"""SELECT sd.query, sd.quantity, groupArray((sd.date, indexOf(sd.products, {product_id}) AS product_index)) AS date_info
        FROM (SELECT rp.query, rp.date, r.quantity, rp.products
        FROM request_product AS rp
        JOIN request AS r ON r.query = rp.query
        WHERE has(rp.products, {product_id})
        AND (rp.city = {city})
        AND (rp.date BETWEEN '{min_date.strftime("%Y-%m-%d")}' AND '{max_date.strftime("%Y-%m-%d")}')
        ORDER BY rp.date, r.quantity DESC
        ) AS sd
        GROUP BY sd.query
        ORDER BY sd.quantity, sd.query;"""
        query_result = await client.query(query)
        result = [
            {
                "query": row[0],
                "quantity": row[1],
            }
        ]



