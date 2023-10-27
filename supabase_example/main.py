import os
import json
import requests
import time
import json

from supabase import create_client, Client

url: str = ""
key: str = ""
supabase: Client = create_client(url, key)

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


@app.get("/financial_data_from_supabase")
def get_financial_data():
    """Get financial data from supabase"""

    try:
        results = supabase.table("financial_data").select("*").execute()

    except Exception as err:
        print(f"Error {err}")

    return results.data
