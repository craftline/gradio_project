from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import requests
import shutil
import uuid
import os
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd

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

@app.post("/split_pdf")
async def split_pdf(pdf: UploadFile = File(...), excel: UploadFile = File(...)):
    temp_pdf = f"temp_{uuid.uuid4().hex}_{pdf.filename}"
    temp_excel = f"temp_{uuid.uuid4().hex}_{excel.filename}"

    with open(temp_pdf, "wb") as f:
        shutil.copyfileobj(pdf.file, f)
    with open(temp_excel, "wb") as f:
        shutil.copyfileobj(excel.file, f)

    results = []
    log_lines = ["🛠️ Splitting files"]
    try:
        reader = PdfReader(temp_pdf)
        df = pd.read_excel(temp_excel)

        required_columns = {"Subject", "start page", "end page"}
        if not required_columns.issubset(set(df.columns)):
            return {"error": f"Excel must contain columns: {', '.join(required_columns)}"}

        for _, row in df.iterrows():
            raw_subject = str(row['Subject']).strip()
            safe_subject = raw_subject.replace('/', '_').replace('\\', '_')
            short_subject = safe_subject.replace('.pdf', '')

            start = int(row['start page']) - 1
            end = int(row['end page'])

            if start < 0 or end > len(reader.pages) or start >= end:
                log_lines.append(f"⚠️ Skipped invalid page range for: {short_subject}")
                continue

            writer = PdfWriter()
            for i in range(start, end):
                writer.add_page(reader.pages[i])

            split_filename = f"split_{uuid.uuid4().hex}_{safe_subject}.pdf"
            writer.write(split_filename)
            log_lines.append(f"📄 Created split file: {short_subject}")

            try:
                log_lines.append(f"🚀 Working on: {short_subject}")
                upload_response = requests.post(
                    url=UPLOAD_URL,
                    headers={"Authorization": WORKFLOW_CONFIG["A"]["api_key"]},
                    files={"file": (split_filename, open(split_filename, "rb"), "application/pdf")},
                    data={"user": "router-user", "type": "document"}
                )
                print("Upload Response:", upload_response.status_code, upload_response.text)

                if upload_response.status_code != 201:
                    log_lines.append(f"❌ Failed to upload {short_subject}: {upload_response.text}")
                    continue

                file_id = upload_response.json().get("id")
                workflow_response = requests.post(
                    url=WORKFLOW_CONFIG["A"]["workflow_url"],
                    headers={
                        "Authorization": WORKFLOW_CONFIG["A"]["api_key"],
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
                print("Workflow Response:", workflow_response.status_code, workflow_response.text)

                if workflow_response.status_code != 200:
                    log_lines.append(f"❌ Workflow failed for {short_subject}: {workflow_response.text}")
                    continue

                result = workflow_response.json()
                output = result.get("data", {}).get("outputs", {}).get("text", "No output returned.")
                results.append({"file": short_subject, "output": output})
                log_lines.append(f"✅ Done: {short_subject}")

            finally:
                if os.path.exists(split_filename):
                    os.remove(split_filename)

    except Exception as e:
        return {"error": str(e)}
    finally:
        os.remove(temp_pdf)
        os.remove(temp_excel)

    if not results:
        log_lines.append("⚠️ لم يتم إنشاء أي ملفات أو لم يتم تلقي مخرجات من النماذج.")

    return {
        "status": "success",
        "results": results,
        "log": "\n".join(log_lines)
    }
