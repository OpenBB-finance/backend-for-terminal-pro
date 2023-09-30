import os
import json
import requests
import time

##python clickhouse integrations https://clickhouse.com/docs/en/integrations/python

import clickhouse_connect

client = clickhouse_connect.get_client(
    host="",
    port=8443,
    username="default",
    password="",
)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

### Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5050",
    "http://localhost:5051",
    "https://pro.openbb.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Endpoints
@app.get("/")
def read_root():
    return {"Info": "Backend Template for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    return JSONResponse(content=data)


@app.get("/click")
def clickhouse():
    """Return clickhouse data"""

    results = client.query_df('SELECT * FROM "nyc_taxi" LIMIT 31')
    # convery df to json
    results_json = results.to_json(orient="records")
    json_obj = json.loads(results_json)

    return json_obj

@app.get("/avg_price_per_year_london")
def avg_price_per_year_london():
    """Return clickhouse data"""

    results = client.query_df(
"""SELECT
   toYear(date) AS year,
   round(avg(price)) AS price
FROM uk_price_paid
WHERE town = 'LONDON'
GROUP BY year
ORDER BY year
""")
    # convery df to json
    results_json = results.to_json(orient="records")
    json_obj = json.loads(results_json)

    return json_obj
