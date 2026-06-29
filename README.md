# Invoice OCR Microservice

AI-powered microservice that accepts invoices (PDF/JPG/PNG), extracts text via OCR, and returns structured JSON using Gemini 2.5 Flash. Consumed by the main .NET app via REST API.

**Status: Phase 3 Complete** (OCR + LLM document understanding)

---

## Quick Start

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your values:
```env
API_KEYS=["demo-key"]
GEMINI_API_KEY=your-gemini-api-key
```

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

---

## API

### `POST /api/v1/process-invoice`
| Header | Value |
|--------|-------|
| `X-API-Key` | Your API key |

Body: `multipart/form-data` with field `file`

**Response:**
```json
{
  "status": "success",
  "data": {
    "header": {
      "company_name": "Acme Corp",
      "invoice_number": "INV-001",
      "gst_number": "29ABCDE1234F1Z5",
      "invoice_date": "2025-06-01",
      "vendor": {"name": "", "address": "", "contact": ""},
      "shipping": {"name": "", "address": "", "vessel": "", "consignee": ""},
      "total_amount": 15000.0,
      "currency": "INR",
      "tax_info": {"tax_type": "GST", "tax_rate": 18.0, "tax_amount": 2700.0}
    },
    "line_items": [
      {"description": "Widget A", "quantity": 10, "unit_price": 500.0, "charges": 200.0, "tax_component": 900.0, "line_total": 5200.0}
    ]
  }
}
```

### `GET /health`
Returns service status + whether LLM is configured.

### `GET /demo`
Browser-based test UI.

---

## Project Structure

```
app/
├── main.py          # FastAPI routes
├── core/config.py   # Env settings
├── middleware/auth.py # X-API-Key validation
├── models/          # Pydantic schemas (request/response)
├── services/
│   ├── ocr.py       # EasyOCR wrapper (PDF/images → raw text)
│   ├── llm.py       # Gemini 2.5 Flash (raw text → structured JSON)
│   └── parser.py    # Pipeline orchestrator
└── utils/pdf.py     # PDF page → image conversion
demo/index.html      # Test UI
```

---

## How It Works

```
Upload → EasyOCR → raw text → Gemini 2.5 Flash → structured JSON → Response
```

Gemini's system prompt handles semantic field mapping (e.g., "Bill No" → `invoice_number`, "Vessel"/"Shipper" → `shipping`).

---

## Tech

| Component | Choice |
|-----------|--------|
| Framework | FastAPI (Python) |
| OCR | EasyOCR (CPU) |
| LLM | Gemini 2.5 Flash |
| PDF | pypdfium2 |
| Auth | X-API-Key header |
| Deployment | TBD (Railway / Docker) |

## .NET Integration

```csharp
client.DefaultRequestHeaders.Add("X-API-Key", "your-key");
var content = new MultipartFormDataContent();
content.Add(new ByteArrayContent(fileBytes), "file", "invoice.pdf");
var response = await client.PostAsync("/api/v1/process-invoice", content);
```
