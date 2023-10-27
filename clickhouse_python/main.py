import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import clickhouse_connect

client = clickhouse_connect.get_client(
    host="",
    port=8443,
    username="default",
    password="",
)

app = FastAPI()

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
    return {"Info": "ClickHouse backend template for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return JSONResponse(content=data)

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
"""
    )
    # convert df to json
    results_json = results.to_json(orient="records")
    json_obj = json.loads(results_json)

    return json_obj
