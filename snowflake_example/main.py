import os
import json
import requests
import time

##python snowflake connector https://docs.snowflake.com/en/developer-guide/python-connector/python-connector
from snowflake.connector import ProgrammingError
import snowflake.connector
import datetime

## Account can be found in Accounts under Admin - ex. https://xxxxxx-xxxxxx.snowflakecomputing.com

conn = snowflake.connector.connect(
    user="",
    password="",
    account="",
    warehouse="COMPUTE_WH",
    database="ECONOMY_DATA_ATLAS",
    schema="ECONOMY",
)


# Define a function to convert Snowflake ResultSet to a JSON-friendly format
def snowflake_to_json(result_set, cur):
    columns = [col[0] for col in cur.description]
    results_list = [dict(zip(columns, row)) for row in result_set]
    return results_list


from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

### Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5050",
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


@app.get("/snowflake")
def get_snowflake_data():
    """Return snowflake data"""

    try:
        cur = conn.cursor()
        cur.execute("select * from DATA_ATLAS limit 10")
        query_id = cur.sfqid
        while conn.is_still_running(conn.get_query_status_throw_if_error(query_id)):
            time.sleep(1)

        results = cur.fetchall()
        print(f"{results}")
    except ProgrammingError as err:
        print("Programming Error: {0}".format(err))

    # Convert the query results to JSON
    json_data = snowflake_to_json(results, cur)

    return json_data
