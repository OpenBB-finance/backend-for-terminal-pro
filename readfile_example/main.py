import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:1420",
    "http://localhost:5050",
    "https://pro.openbb.dev",
    "https://pro.openbb.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ROOT_PATH = Path(__file__).parent.resolve()


@app.get("/")
def read_root():
    return {"Info": "Read file example for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    return JSONResponse(content=json.load((ROOT_PATH / "widgets.json").open()))


@app.get("/json-data")
def json_data():
    """Read mock csv data and return it as a table to your widget"""
    # Specify the path to your JSON file
    json_file_path = "mock_data.json"

    try:
        # Return the JSON data as is
        return json.load((ROOT_PATH / json_file_path).open()).get("stocks", [])
    except Exception as e:
        # Handle error cases here
        error_message = f"Error reading the JSON file: {str(e)}"
        return JSONResponse(content={"error": error_message}, status_code=500)


@app.get("/csv-data")
def csv_data():
    """Read mock csv data and return it as a table to your widget"""
    # Specify the path to your CSV file
    csv_file_path = "mock_data.csv"

    try:
        # Convert the DataFrame to a dictionary and return the data
        return pd.read_csv((ROOT_PATH / csv_file_path).open()).to_dict(orient="records")
    except Exception as e:
        # Handle error cases here
        error_message = f"Error reading the CSV file: {str(e)}"
        return JSONResponse(content={"error": error_message}, status_code=500)
