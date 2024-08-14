import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import time
import numpy as np
import pandas as pd
from datetime import datetime
# import arcticdb as adb

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

# # For this demo we will configure the LMDB file based backend. ArcticDB achieves its high performance and scale when configured with an object store backend (e.g. S3).
# arctic = adb.Arctic("lmdb://arcticdb_demo")

# # You can have an unlimited number of libraries, but we will just create one to start with.
# lib = arctic.get_library('sample', create_if_missing=True)

# n = 10_000
# large = pd.DataFrame(
#     np.linspace(1, n, n)*np.linspace(1, n, n)[:,np.newaxis],
#     columns=[f'c{i}' for i in range(n)],
#     index=pd.date_range('1/1/2020', periods=n, freq="H")
# )
# lib.write('large', large)

@app.get("/")
def read_root():
    return {"Info": "ArcticDB backend template for the OpenBB Terminal Pro"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Terminal Pro"""
    return JSONResponse(
        content=json.load((Path(__file__).parent.resolve() / "widgets.json").open())
    )

# Using the example from https://colab.research.google.com/github/man-group/ArcticDB/blob/master/docs/mkdocs/docs/notebooks/ArcticDB_demo_lmdb.ipynb#scrollTo=g7oLl_YlQqeM

@app.get("/large_dataframe")
def large_dataframe():

    # Generate random data for the specified columns
    data = {
        'c0': np.random.rand(5),
        'c1': np.random.rand(5),
        'c5000': np.random.rand(5),
        'c5001': np.random.rand(5),
        'c9998': np.random.rand(5),
        'c9999': np.random.rand(5)
    }

    # Create datetime index
    date_range = pd.date_range(start='2020-06-13 08:00:00', periods=5, freq='H')

    # Create the dataframe
    subframe = pd.DataFrame(data, index=date_range)
    subframe = subframe.reset_index().rename(columns={'index': 'date'})

    # Read the subframe from the random dataframe
    # subframe = lib.read(
    #     "large",
    #     columns=["c0", "c1", "c5000", "c5001", "c9998", "c9999"],
    #     date_range=(datetime(2020, 6, 13, 8), datetime(2020, 6, 13, 13))
    # ).data

    # convert df to json
    return subframe.to_dict(orient="records")
