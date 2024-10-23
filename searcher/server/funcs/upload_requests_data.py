from datetime import datetime

from sqlalchemy import delete

from db import Request
from db.base import async_session_maker
from settings import logger, TIMEZONE



async def upload_requests_worker(request, now_date):



async def upload_requests_csv_bg(requests_data: list[list[str|int]]):
    logger.info("Uploading requests data")
    now_date = datetime.now(TIMEZONE).date()

    async with async_session_maker() as session:
        logger.info("Start of DB renewal")
        for row in requests_data:
            try:
                await session.merge(Request(query=row[0], quantity=row[1], updated_at=now_date))
            except Exception as e:
                logger.error(f"{e}")
    logger.warning("DB renewal complete")
