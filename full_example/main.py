import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from plotly_templates import dark_template

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
    return {"Info": "Full example for OpenBB Custom Backend"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Custom Backend"""
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

        # Sort the DataFrame by 'tvl' in descending order and select the top 30
        top_30_df = df.sort_values(by='tvl', ascending=False).head(30)

        # Create a bar chart using Plotly
        figure = go.Figure(
            data=[go.Bar(x=top_30_df["tokenSymbol"], y=top_30_df["tvl"])],
            # Apply the dark template - see plotly_templates.py
            layout=go.Layout(
                template=dark_template,
                title="Top 30 Chains by TVL",
                xaxis_title="Token Symbol",
                yaxis_title="Total Value Locked (TVL)"
            )
        )

        # return the plotly json
        return json.loads(figure.to_json())

    print(f"Request error {response.status_code}: {response.text}")
    return JSONResponse(
        content={"error": response.text}, status_code=response.status_code
    )


@app.get("/historical_chains")
def get_historical_chains(chain: str = None):
    """Get historical TVL of a chain using Defi LLama"""

    if chain is None:
        chain = "Ethereum"
    response = requests.get(f'https://api.llama.fi/v2/historicalChainTvl/{chain}')

    if response.status_code == 200:
        return response.json()

    print(f"Request error {response.status_code}: {response.text}")
    return JSONResponse(
        content={"error": response.text}, status_code=response.status_code
    )

# Fetching list of chains for a parameter in the widget
@app.get("/get_chains_list")
def get_chains_list():
    """Get list of chains using Defi LLama"""
    response = requests.get("https://api.llama.fi/v2/chains")

    if response.status_code == 200:
        data = response.json()
        # can pass as list of {label, value} for dropdown or list of strings
        #  [
        #   {"label": chain.get("name"), "value": chain.get("name")}
        #   for chain in data if chain.get("name")
        #  ]
        return [chain.get("name") for chain in data if chain.get("name")]

    print(f"Request error {response.status_code}: {response.text}")
    return JSONResponse(
        content={"error": response.text}, status_code=response.status_code
    )

@app.get("/show_example_params")
def show_example_params(datePicker1: str = None, textBox1: str = None, daysPicker1: str = "1"):
    """Show example of how to use parameters in the URL"""

    return {"datePicker1": datePicker1, "textBox1": textBox1, "daysPicker1": daysPicker1.split(",")}


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
