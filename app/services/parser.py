from app.models.response import InvoiceResponse
from app.services.llm import LLMService
from app.services.ocr import OCRService


class InvoiceParser:
    def __init__(self):
        self.ocr = OCRService()
        self.llm = LLMService()

    def process(self, file_bytes: bytes, filename: str) -> InvoiceResponse:
        raw_text = self.ocr.extract_text(file_bytes, filename)

        if not raw_text.strip():
            return InvoiceResponse(
                status="error",
                data={
                    "header": {
                        "company_name": "",
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

        if self.llm.is_available():
            return self.llm.extract_invoice(raw_text)

        return self.llm._fallback_response(raw_text)
