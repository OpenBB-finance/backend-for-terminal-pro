import json
import requests
import plotly.express as px
import pandas as pd

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
    return {"Info": "Plotly example for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return JSONResponse(content=data)


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

    print(f"Request error {response.status_code}: {response.text}")
    return None
