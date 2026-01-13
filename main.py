import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from report import create_parliamentary_report

app = FastAPI(title="Raqabi Backend")

class Payload(BaseModel):
    title: str
    data: list
    analysis: str
    sector: str = ""
    entity: str = ""
    risk: str = ""
    action: str = ""
    author: str = ""

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate-report")
def generate_report(payload: Payload):
    file_path = create_parliamentary_report(
        report_title=payload.title,
        data_list=payload.data,
        ai_analysis=payload.analysis,
        sector=payload.sector,
        entity=payload.entity,
        risk=payload.risk,
        proposed_action=payload.action,
        author=payload.author,
        out_dir="reports"
    )

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(file_path),
    )
