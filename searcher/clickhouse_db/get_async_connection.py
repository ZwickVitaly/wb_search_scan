from contextlib import asynccontextmanager
import clickhouse_connect
from clickhouse_connect.driver.asyncclient import AsyncClient
from settings import CLICKHOUSE_CONFING

@asynccontextmanager
async def get_async_connection() -> AsyncClient:
    client = await clickhouse_connect.get_async_client(**CLICKHOUSE_CONFING)
    yield client
    client.close()