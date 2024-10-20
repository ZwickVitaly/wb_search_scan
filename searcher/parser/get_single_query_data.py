import asyncio
from json import JSONDecodeError

from aiohttp import ClientSession, ContentTypeError, client_exceptions, ClientTimeout

from settings import SEARCH_URL, logger


async def get_query_data(http_session: ClientSession, query_string, dest, limit, page, rqa=5, timeout=5):
    _data = {}
    counter = 0
    while (not _data.get("data") or len(_data.get("data").get("products")) < 2) and counter < rqa:
        counter += 1
        logger.info(f"{counter} -> {query_string}")
        try:
            async with http_session.get(
                url=SEARCH_URL,
                params={
                    "resultset": "catalog",
                    "query": query_string,
                    "limit": limit,
                    "dest": dest,
                    "page": page,
                },
                timeout=timeout,
            ) as response:
                if response.ok:
                    try:
                        _data = await response.json(content_type="text/plain")
                    except ContentTypeError:
                        return {"data": {"products": []}}
                else:
                    logger.critical("response not ok")
                    continue
        except (ContentTypeError, TypeError, JSONDecodeError, client_exceptions.ServerDisconnectedError, asyncio.TimeoutError) as e:
            logger.critical(f"ОШИБКА, {type(e)}")
            counter -= 1
            timeout += 1
            await asyncio.sleep(0.01)
            continue

    return _data.get("data")


# взято с https://user-geo-data.wildberries.ru/get-geo-info?latitude=[ШИРОТА float]&longitude=[ДОЛГОТА float]
# Москва -1257786
# Краснодар 12358063
# Екатеринбург -5817698
# Владивосток 123587791
