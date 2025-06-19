from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import requests
import shutil
import uuid
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WORKFLOW_CONFIG = {
    "A": {
        "api_key": os.getenv("WORKFLOW_A_KEY"),
        "workflow_url": os.getenv("WORKFLOW_A_URL")
    },
    "B": {
        "api_key": os.getenv("WORKFLOW_B_KEY"),
        "workflow_url": os.getenv("WORKFLOW_B_URL")
    },
    "C": {
        "api_key": os.getenv("WORKFLOW_C_KEY"),
        "workflow_url": os.getenv("WORKFLOW_C_URL")
    },
    "D": {
        "api_key": os.getenv("WORKFLOW_D_KEY"),
        "workflow_url": os.getenv("WORKFLOW_D_URL")
    }
}

UPLOAD_URL = os.getenv("UPLOAD_URL")

@app.post("/process")
async def process_file(route: str = Form(...), file: UploadFile = File(...)):
    route = route.upper()
    if route not in WORKFLOW_CONFIG:
        return JSONResponse(status_code=400, content={"error": "Invalid route. Use A or B."})

    temp_filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        upload_response = requests.post(
            url=UPLOAD_URL,
            headers={"Authorization": WORKFLOW_CONFIG[route]["api_key"]},
            files={"file": (file.filename, open(temp_filename, "rb"), file.content_type)},
            data={"user": "router-user", "type": "document"}
        )
    finally:
        os.remove(temp_filename)

    if upload_response.status_code != 201:
        return JSONResponse(status_code=upload_response.status_code, content={"error": "File upload failed", "details": upload_response.text})

    file_id = upload_response.json().get("id")

    workflow_response = requests.post(
        url=WORKFLOW_CONFIG[route]["workflow_url"],
        headers={
            "Authorization": WORKFLOW_CONFIG[route]["api_key"],
            "Content-Type": "application/json"
        },
        json={
            "inputs": {
                "pdffile": {
                    "transfer_method": "local_file",
                    "upload_file_id": file_id,
                    "type": "document"
                }
            },
            "response_mode": "blocking",
            "user": "router-user"
        }
    )

    if workflow_response.status_code != 200:
        return JSONResponse(status_code=workflow_response.status_code, content={"error": "Workflow execution failed", "details": workflow_response.text})

    result = workflow_response.json()
    return result.get("data", {}).get("outputs", {}).get("text", "No output returned.")

