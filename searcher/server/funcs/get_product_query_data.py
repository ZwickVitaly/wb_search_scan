from clickhouse_db.get_async_connection import get_async_connection
from datetime import date


async def get_db_data(product_id, dates_list, city):
    max_date: date = max(dates_list)
    min_date: date = min(dates_list)
    async with get_async_connection() as client:
        query = f"""SELECT sd.query, sd.quantity, groupArray((sd.date, indexOf(sd.products, {product_id}) AS product_index)) AS date_info
        FROM (SELECT rp.query, rp.date, r.quantity, rp.products
        FROM request_product AS rp
        JOIN (SELECT * FROM request FINAL) AS r ON r.query = rp.query
        WHERE has(rp.products, {product_id})
        AND (rp.city = {city})
        AND (rp.date BETWEEN '{min_date.strftime("%Y-%m-%d")}' AND '{max_date.strftime("%Y-%m-%d")}')
        ORDER BY rp.date, r.quantity DESC
        ) AS sd
        GROUP BY sd.query, sd.quantity
        ORDER BY sd.quantity DESC, sd.query;"""
        query_result = await client.query(query)
        result = [
            {
                "query": row[0],
                "quantity": row[1],
                "dates": {
                    str(j_row[0]): j_row[1]
                    for j_row in row[3]
                }
            }
            for row in query_result.result_rows
        ]
        return result



