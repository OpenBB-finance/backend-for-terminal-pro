import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import requests
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
    "https://excel.openbb.co",
    "https://excel.openbb.dev",
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
    return {"Info": "Plotly example for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    return JSONResponse(
        content=json.load((Path(__file__).parent.resolve() / "widgets.json").open())
    )


@app.get("/chains")
def get_chains():
    """Get current TVL of all chains using Defi LLama"""
    params = {}
    response = requests.get("https://api.llama.fi/v2/chains", params=params)

    if response.status_code == 200:
        # Create a DataFrame from the JSON data
        df = pd.DataFrame(response.json())

        # Create a bar chart using Plotly
        figure = go.Figure(
            layout=dict(yaxis=dict(title="TVL"), margin=dict(b=50, l=10, r=40, t=0))
        )
        figure.add_bar(x=df["tokenSymbol"], y=df["tvl"])

        # return the plotly json
        return json.loads(figure.to_json())

    print(f"Request error {response.status_code}: {response.text}")
    return JSONResponse(
        content={"error": response.text}, status_code=response.status_code
    )


@app.get("/chains_table")
def chains_table():
    """Get current TVL of all chains using Defi LLama"""
    params = {}
    response = requests.get("https://api.llama.fi/v2/chains", params=params)

    if response.status_code == 200:
        return response.json()

    print(f"Request error {response.status_code}: {response.text}")
    return JSONResponse(
        content={"error": response.text}, status_code=response.status_code
    )


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
