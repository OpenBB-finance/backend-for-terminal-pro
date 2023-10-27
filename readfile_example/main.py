import json
import csv

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:1420",
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


@app.get("/")
def read_root():
    return {"Info": "Read file example for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
    return JSONResponse(content=data)

@app.get("/json-data")
def json_data():
    """Read mock csv data and return it as a table to your widget"""
    # Specify the path to your JSON file
    json_file_path = "mock_data.json"

    try:
        # Open the JSON file for reading
        with open(json_file_path, mode="r", encoding='utf-8') as json_file:
            # Load the JSON data
            chains_data = json.load(json_file)

        # Return the JSON data as is
        return chains_data["stocks"]

    except Exception as e:
        # Handle error cases here
        error_message = f"Error reading the JSON file: {str(e)}"
        return {"error": error_message}


@app.get("/csv-data")
def csv_data():
    """Read mock csv data and return it as a table to your widget"""
    # Specify the path to your CSV file
    csv_file_path = "mock_data.csv"

    try:
        # Open the CSV file for reading
        with open(csv_file_path, mode="r", encoding='utf-8') as csv_file:
            # Create a CSV reader
            csv_reader = csv.DictReader(csv_file)

            # Initialize an empty list to store CSV data
            chains_data = []

            # Iterate through each row in the CSV file
            for row in csv_reader:
                # Append each row (as a dictionary) to the list
                chains_data.append(row)

        # Return the CSV data as JSON response
        return json.loads(json.dumps(chains_data))

    except Exception as e:
        # Handle error cases here
        error_message = f"Error reading the CSV file: {str(e)}"
        return {"error": error_message}
