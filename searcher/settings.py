import os
from os import getenv
from pathlib import Path
from sys import stdout
from dotenv import load_dotenv

from loguru import logger

# from pytz import timezone
load_dotenv()

DEBUG = getenv("DEBUG", "1") == "1"

BASE_DIR = Path(__file__).parent

logger.remove()
logger.add(
    "app_data/logs/debug_logs.log" if DEBUG else "app_data/logs/bot.log",
    rotation="00:00:00",
    level="DEBUG" if DEBUG else "INFO",
)
logger.add(stdout, level="DEBUG" if DEBUG else "INFO")



SEARCH_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"

POPULAR_REQUESTS_URL = "https://seller.wildberries.ru/popular-search-requests"

GEOCODING_URL = "https://openweathermap.org/api/geocoding-api"


POSTGRES_CONFIG = {
    "driver": "postgresql+asyncpg",
    "username": os.getenv("PG_USER", "admin"),
    "password": os.getenv("PG_PASSWORD", "admin321"),
    "database": os.getenv("PG_DATABASE", "admin"),
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432")

}

