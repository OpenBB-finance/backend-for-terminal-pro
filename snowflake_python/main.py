import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from snowflake.connector import ProgrammingError
import snowflake.connector

# Data from: https://app.snowflake.com/marketplace/listing/GZTSZAS2KIM/cybersyn-inc-cybersyn-weather-environmental-essentials?search=cybersin&sortBy=relevant&pricing=free

conn = snowflake.connector.connect(
    user="",
    password="",
    account="",
    warehouse="COMPUTE_WH",
    database="Cybersyn_Weather__Environmental_Essentials",
    schema="CYBERSIN",
)

# Define a function to convert Snowflake ResultSet to a JSON-friendly format
def snowflake_to_json(result_set, cur):
    columns = [col[0] for col in cur.description]
    results_list = [dict(zip(columns, row)) for row in result_set]
    return results_list

app = FastAPI()

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
    return {"Info": "Snowflake backend template for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return JSONResponse(content=data)


@app.get("/cybersyn_severe_weather_days_in_florida")
def get_cybersyn_severe_weather_days_in_florida():
    """Return snowflake data"""

    try:
        cur = conn.cursor()
        cur.execute("""
SELECT
    YEAR(ts.date) AS year,
    COUNT(DISTINCT ts.date) AS count_severe_weather_days
FROM cybersyn.noaa_weather_metrics_timeseries AS ts
JOIN cybersyn.noaa_weather_station_index AS idx
    ON (ts.noaa_weather_station_id = idx.noaa_weather_station_id)
WHERE 
    ts.variable_name = 'Weather Type: Tornado, Waterspout, or Funnel Cloud'
    AND idx.state_name = 'Florida'
    AND ts.value = 1
    AND ts.date >= '2010-01-01'
GROUP BY year
ORDER BY year;
        """)
        results = cur.fetchall()
    except ProgrammingError as err:
        print("Programming Error: {0}".format(err))

    # Convert the query results to JSON
    json_data = snowflake_to_json(results, cur)

    return json_data
