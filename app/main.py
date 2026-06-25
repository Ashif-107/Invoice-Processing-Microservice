from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.middleware.auth import APIKeyMiddleware
from app.models.response import InvoiceResponse, InvoiceData, HeaderInfo, VendorInfo, ShippingInfo, TaxInfo, LineItem

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(APIKeyMiddleware)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/demo", response_class=HTMLResponse)
def demo():
    html_path = Path(__file__).resolve().parent.parent / "demo" / "index.html"  
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/api/v1/process-invoice", response_model=InvoiceResponse)
async def process_invoice(file: UploadFile = File(...)):
    return InvoiceResponse(
        status="success",
        data=InvoiceData(
            header=HeaderInfo(
                company_name="Acme Corp",
                invoice_number="INV-001",
                gst_number="29ABCDE1234F1Z5",
                invoice_date="2025-06-01",
                vendor=VendorInfo(
                    name="Vendor Ltd",
                    address="123 Business Park, Mumbai",
                    contact="info@vendor.com",
                ),
                shipping=ShippingInfo(
                    name="ShipCo Logistics",
                    address="456 Port Road, Chennai",
                    vessel="MV Ocean Explorer",
                    consignee="John Doe",
                ),
                total_amount=15000.00,
                currency="INR",
                tax_info=TaxInfo(
                    tax_type="GST",
                    tax_rate=18.0,
                    tax_amount=2700.00,
                ),
            ),
            line_items=[
                LineItem(
                    description="Widget A - Premium Quality",
                    quantity=10.0,
                    unit_price=500.00,
                    charges=200.00,
                    tax_component=900.00,
                    line_total=5200.00,
                ),
                LineItem(
                    description="Widget B - Standard",
                    quantity=20.0,
                    unit_price=300.00,
                    charges=150.00,
                    tax_component=1080.00,
                    line_total=7230.00,
                ),
            ],
        ),
    )
