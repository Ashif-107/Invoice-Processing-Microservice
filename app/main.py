from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.middleware.auth import APIKeyMiddleware
from app.models.response import InvoiceResponse
from app.services.ocr import OCRService

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(APIKeyMiddleware)

ocr_service = OCRService()


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/demo", response_class=HTMLResponse)
def demo():
    html_path = Path(__file__).resolve().parent.parent / "demo" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/api/v1/process-invoice", response_model=InvoiceResponse)
async def process_invoice(file: UploadFile = File(...)):
    file_bytes = await file.read()
    raw_text = ocr_service.extract_text(file_bytes, file.filename or "file")

    print("===== OCR START =====")
    print(raw_text)
    print("===== OCR END =====")
    return InvoiceResponse(
        status="success",
        data={
            "header": {
                "company_name": raw_text[:100],
                "invoice_number": "",
                "gst_number": "",
                "invoice_date": "",
                "vendor": {"name": "", "address": "", "contact": ""},
                "shipping": {"name": "", "address": "", "vessel": "", "consignee": ""},
                "total_amount": 0.0,
                "currency": "",
                "tax_info": {"tax_type": "", "tax_rate": 0.0, "tax_amount": 0.0},
            },
            "line_items": [],
        },
    )
