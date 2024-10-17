from fastapi import FastAPI

from server.routers.load_csv import csv_router

app = FastAPI()


app.include_router(csv_router, prefix="/api/csv")