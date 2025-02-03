import base64
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

origins = ["https://pro.openbb.co", "https://excel.openbb.co", "http://localhost:1420"]

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
    return {"Info": "PDF Widget Example"}


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for the OpenBB Custom Backend."""
    return JSONResponse(content=json.load((ROOT_PATH / "widgets.json").open()))


@app.get("/files-base64")
def get_files_base64(name: str):
    """Serve a file through base64 encoding."""
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
                "filename": name,
            },
            "content": content,
        },
    )


@app.get("/files-url")
def get_files_url(name: str):
    """Serve a file through URL."""
    FILES = {
        "openbb-story.pdf": "https://openbb-assets.s3.us-east-1.amazonaws.com/pro-file-storage/00060c82-2ceb-4161-b5c0-ebb66a83e8f2.pdf",
        # Using the local file as AI context only works if this backend is deployed and publicly accessible.
        "sample.pdf": "http://localhost:5050/files-raw?name=sample.pdf",
    }
    file_reference = FILES.get(name)
    if not file_reference:
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse(
        headers={"Content-Type": "application/json"},
        content={
            "data_format": {
                "data_type": "pdf",
                "filename": name,
            },
            "file_reference": file_reference,
        },
    )


@app.get("/files-raw")
def get_files_raw(name: str):
    """Example of serving a file from a local URL."""
    try:
        return FileResponse(
            path=ROOT_PATH / name, media_type="application/pdf", filename=name
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=5050, reload=True)
