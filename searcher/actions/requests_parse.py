import asyncio

from parser.parser_main import get_results
from celery_main import celery_app


@celery_app.task(name="parse_wb_search")
def parse_wb_search():
    asyncio.run(get_results())