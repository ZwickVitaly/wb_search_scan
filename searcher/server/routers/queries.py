from fastapi import APIRouter
from fastapi.params import Body, Query
from fastapi.responses import JSONResponse

from clickhouse_db.get_async_connection import get_async_connection
from settings import logger


query_router = APIRouter()


@query_router.get("/product_queries")
async def get_product_queries(product_id: int = Query()):
    ...


@query_router.post("/get_keywords")
async def get_products_queries(products_ids: list[int] = Body()):
    ...
