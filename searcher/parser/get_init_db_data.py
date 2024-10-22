from sqlalchemy import select
from db.base import async_session_maker
from db import City, Request



async def get_cities_data():
    async with async_session_maker() as s:
        q = await s.execute(select(City))
        cities = q.scalars()
    return cities


async def get_requests_data():
    async with async_session_maker() as s:
        q = await s.execute(select(Request).order_by(Request.quantity.desc()))
        requests = q.scalars()
    return requests
