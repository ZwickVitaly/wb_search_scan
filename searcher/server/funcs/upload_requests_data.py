from sqlalchemy import delete

from db import Request
from db.base import async_session_maker
from settings import logger


async def upload_requests_csv_bg(requests_data: list[list[str|int]]):
    logger.info("Uploading requests data")
    async with async_session_maker() as session:
        await session.execute(delete(Request))
        await session.commit()
    logger.info("Requests db purged")
    async with async_session_maker() as session:
        logger.info("Start of DB renewal")
        session.add_all([Request(query=row[0], quantity=row[1]) for row in requests_data])
        await session.commit()
    logger.warning("DB renewal complete")
