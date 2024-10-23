from asyncio import TaskGroup
from datetime import datetime
from db import Request
from db.base import async_session_maker
from settings import logger, TIMEZONE



async def upload_requests_worker(requests_slice, now_date):
    async with async_session_maker() as session:
        logger.info("Start of DB renewal")
        for row in requests_slice:
            try:
                await session.merge(Request(query=row.get("query"), quantity=row.get("quantity")))
            except Exception as e:
                logger.error(f"{e}")
        await session.commit()


async def upload_requests_csv_bg(requests_data: list[dict]):
    logger.info("Uploading requests data")
    now_date = datetime.now(TIMEZONE).date()
    async with TaskGroup() as tg:
        tg.create_task(upload_requests_worker(requests_data[:250000], now_date))
        tg.create_task(upload_requests_worker(requests_data[250000:500000], now_date))
        tg.create_task(upload_requests_worker(requests_data[500000:750000], now_date))
        tg.create_task(upload_requests_worker(requests_data[750000:], now_date))
    logger.warning("DB renewal complete")
