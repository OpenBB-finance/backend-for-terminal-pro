import os
import json
import requests

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

## Routes
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

@app.get("/chains")
def get_player_list():
    """Get current TVL of all chains using Defi LLama"""
    params = {}
    response = requests.get("https://api.llama.fi/v2/chains", params=params)

    if response.status_code == 200:
        return response.json()
    
    # Handle error cases here
    print(f"Something went wrong with the request : Error {response.status_code}: {response.text}")
    return None

