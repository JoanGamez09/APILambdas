import sys
import os

# Agregar la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from mangum import Mangum
from app.module_data.data import get_data, get_data_json, get_data_csv

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!2"}

@app.get("/data")
async def get_json_data():
    response = get_data()
    return response

@app.get("/data/resume")
async def get_processed_data():
    response = get_data_json()
    return response


@app.get("/data/processed/{year}/{month}/{day}")
async def get_processed_data(year: int, month: int, day: int):
    response = get_data_csv(year, month, day)
    return response


handler = Mangum(app)


