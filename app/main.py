from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.middleware.auth import APIKeyMiddleware
from app.models.response import InvoiceResponse
from app.services.parser import InvoiceParser

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(APIKeyMiddleware)

parser = InvoiceParser()


@app.get("/health")
def health():
    llm_ok = parser.llm.is_available()
    return {
        "status": "ok",
        "service": settings.app_name,
        "llm_configured": llm_ok,
    }


@app.get("/demo", response_class=HTMLResponse)
def demo():
    html_path = Path(__file__).resolve().parent.parent / "demo" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/api/v1/process-invoice", response_model=InvoiceResponse)
async def process_invoice(file: UploadFile = File(...)):
    file_bytes = await file.read()
    result = parser.process(file_bytes, file.filename or "file")
    return result
