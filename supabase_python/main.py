import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from supabase import create_client, Client

supabase: Client = create_client(
    url="",
    key=""
)

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
    return {"Info": "Supabase backend template for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    file_path = "widgets.json"
    with open(file_path, "r", encoding='utf-8') as file:
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
