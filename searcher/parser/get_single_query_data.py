import asyncio
from json import JSONDecodeError

from aiohttp import ClientSession, ContentTypeError, client_exceptions, ClientTimeout

from settings import SEARCH_URL, logger


async def get_query_data(query_string, dest, limit, page, rqa=5, timeout=10):
    _data = {}
    counter = 0
    async with ClientSession() as session:
        while (not _data.get("data") or len(_data.get("data").get("products")) < 2) and counter < rqa:
            counter += 1
            logger.info(f"{counter} -> {query_string}")
            try:
                async with session.get(
                    url=SEARCH_URL,
                    params={
                        "resultset": "catalog",
                        "query": query_string,
                        "limit": limit,
                        "dest": dest,
                        "page": page,
                    },
                    timeout=timeout
                ) as response:
                    if response.ok:
                        _data = await response.json(content_type="text/plain")
            except (ContentTypeError, TypeError, JSONDecodeError):
                raise ValueError(
                    "Плохой ответ от ВБ, данные:\n"
                    f"query_string: {query_string}\n"
                    f"dest: {dest}\n"
                    f"limit: {limit}\n"
                    f"page: {page}\n"
                    f"rqa: {rqa}"
                )
            except (client_exceptions.ServerDisconnectedError, asyncio.TimeoutError):
                logger.critical("ТАЙМАУТ или клиент")
                await asyncio.sleep(1)
                counter -= 1
                continue
        await session.close()
        return _data.get("data")


# взято с https://user-geo-data.wildberries.ru/get-geo-info?latitude=[ШИРОТА float]&longitude=[ДОЛГОТА float]
# Москва -1257786
# Краснодар 12358063
# Екатеринбург -5817698
# Владивосток 123587791
