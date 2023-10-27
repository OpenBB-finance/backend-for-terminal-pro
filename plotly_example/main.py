import os
import json
import requests
import plotly.express as px
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

### Configure CORS
origins = [
    "http://localhost",
    "http://localhost:1420",
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


## Example of return a plotly to json and having that work
@app.get("/chains")
def get_chains():
    """Get current TVL of all chains using Defi LLama"""
    params = {}
    response = requests.get("https://api.llama.fi/v2/chains", params=params)

    if response.status_code == 200:

        # Create a DataFrame from the JSON data
        df = pd.DataFrame(response.json())

        # Create a bar chart using Plotly Express
        fig = px.bar(df, x="tokenSymbol", y="tvl", title="TVL of Tokens")
        fig.update_layout(
            margin={
                "b": 80,
            }
        )
        fig.update_yaxes(title="TVL")
        figure_dict = fig.to_json()
        figure_json = json.loads(figure_dict)
        return figure_json

    # return the plotly json

    # Handle error cases here
    print(
        f"Something went wrong with the request : Error {response.status_code}: {response.text}"
    )
    return None
