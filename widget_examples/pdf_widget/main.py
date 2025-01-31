import base64
import json
from pathlib import Path
from textwrap import dedent
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "https://pro.openbb.co",
    "https://excel.openbb.co",
    "http://localhost:1420"
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

@app.get("/files-base64")
def get_files(name: str):
    """Serve a file through base64 encoding"""
    try:
        with open(ROOT_PATH / name, "rb") as file:
            file_data = file.read()
            encoded_data = base64.b64encode(file_data)
            content = encoded_data.decode("utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse(
        headers={"Content-Type": "application/json"},
        content={
            "data_format": {
                "data_type": "pdf",
                "filename": f"{name}",
            },
            "content": content
        }
    )

@app.get("/files-url")
def get_files_url(name: str):
    """Serve a file through URL"""
    FILES = {
        "sample.pdf": "https://pdfobject.com/pdf/sample.pdf",
        "other-sample.pdf": "https://ontheline.trincoll.edu/images/bookdown/sample-local-pdf.pdf",
    }
    file_reference = FILES.get(name)
    if not file_reference:
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse(
        headers={"Content-Type": "application/json"},
        content={
            "data_format": {
                "data_type": "pdf",
                "filename": f"{name}",
            },
            "file_reference": file_reference,
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5050, reload=True)