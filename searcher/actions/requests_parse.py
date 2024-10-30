from celery import Celery
from celery.schedules import crontab
from parser.parser_main import get_results

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
async def parse_wb_search():
    await get_results()

app.conf.beat_schedule = {
    'run-every-day-at-22:00': {
        'task': 'actions.requests_parse.parse_wb_search',
        'schedule': crontab(hour=22, minute=0, tz='Europe/Moscow'),
    },
}