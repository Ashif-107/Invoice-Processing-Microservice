import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.models.response import InvoiceResponse

SYSTEM_PROMPT = """
You are an invoice data extraction expert. Extract structured data from the OCR text of an invoice.

Field mapping rules — map these variations to the standard fields:
- Invoice Number: "Invoice No", "Bill No", "Invoice #", "Reference", "Document No", "Bill Number"
- GST Number: "GST", "GSTIN", "GST Registration No", "Tax ID", "GST No"
- Invoice Date: "Date", "Invoice Date", "Bill Date", "Issue Date", "Document Date"
- Company Name: "Seller", "Supplier", "Vendor", "From", "Bill From", "Shipper"
- Total Amount: "Total", "Grand Total", "Amount Due", "Net Payable", "Total Amount"
- Tax: "GST", "VAT", "Sales Tax", "Tax Amount", "IGST", "CGST", "SGST"
- Currency: Look for INR, USD, $, ₹ symbols

Shipping invoice fields:
- "Vessel", "Vessel Name", "MV" → shipping.vessel
- "Shipper", "Exporter" → shipping.name
- "Consignee", "Importer", "Buyer" → shipping.consignee
- "Port of Loading", "Port of Discharge" → include in shipping.address

Line items — extract these details for each product or service:
- description, quantity, unit_price, charges, tax_component, line_total

Rules:
1. Return ONLY valid JSON matching the schema. No markdown, no explanation.
2. If a field is not found in the text, leave it as null or empty string.
3. Normalize dates to YYYY-MM-DD format.
4. Parse numeric values as numbers (not strings).
5. Be thorough — extract every line item visible in the invoice.
"""


class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def is_available(self) -> bool:
        return self.client is not None

    def extract_invoice(self, raw_text: str) -> InvoiceResponse:
        if not self.client:
            return self._fallback_response(raw_text)

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Extract invoice data from the following OCR text:\n\n{raw_text}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    response_schema=InvoiceResponse,
                    temperature=0.1,
                ),
            )

            return response.parsed

        except Exception as e:
            print(f"[LLM Error] {e}")
            return self._fallback_response(raw_text)

    def _fallback_response(self, raw_text: str) -> InvoiceResponse:
        data = {
            "status": "partial",
            "data": {
                "header": {
                    "company_name": raw_text[:200],
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
        }
        return InvoiceResponse(**data)
