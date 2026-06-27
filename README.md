# Invoice OCR Microservice

An AI-powered document intelligence microservice that accepts invoice documents (PDF, JPG, PNG), extracts text via OCR, and returns structured JSON. Designed to be consumed by the main .NET application through REST APIs.

---

## Architecture

```
.NET App (separate project)
     │
     │  POST /api/v1/process-invoice
     │  Headers: X-API-Key: <secret>
     │  Body: multipart/form-data (file)
     ▼
OCR Microservice (FastAPI)
     │
     ├── Middleware → API Key validation (X-API-Key header)
     │
     ├── PDF → pypdfium2 → images → EasyOCR → raw text
     ├── PNG / JPG → EasyOCR → raw text
     │
     ├── [Phase 3] Gemini 2.5 Flash → structured JSON
     │
     ▼
JSON Response returned to .NET App
```

---

## Project Structure

```
invoice-processor/
├── app/
│   ├── main.py                 # FastAPI app — routes: /health, /demo, /api/v1/process-invoice
│   ├── core/
│   │   └── config.py           # Environment settings (API keys, app name, debug mode)
│   ├── middleware/
│   │   └── auth.py             # X-API-Key header validation
│   ├── models/
│   │   ├── request.py          # Upload request model
│   │   └── response.py         # Pydantic schemas for invoice JSON response
│   ├── services/
│   │   └── ocr.py              # OCRService — wraps EasyOCR, handles PDF & images
│   └── utils/
│       └── pdf.py              # pdf_to_images() — renders PDF pages to PIL images
├── demo/
│   └── index.html              # Browser-based test UI (simulates the .NET app)
├── tests/                      # Test files (placeholder)
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata
├── Dockerfile                  # Docker config (Phase 4)
├── railway.json                # Railway deploy config (Phase 4)
└── .env                        # Environment variables (not committed to git)
```

---

## Current Status (Phase 2 Complete)

### What's Working

| Feature | Status | Details |
|---------|--------|---------|
| FastAPI server | ✅ | Routes, middleware, error handling |
| API Key auth | ✅ | X-API-Key header validated on all routes except /health and /demo |
| File upload | ✅ | Multipart form-data, any file type |
| OCR - Images (PNG/JPG) | ✅ | EasyOCR extracts text from images |
| OCR - PDF | ✅ | pypdfium2 renders pages → EasyOCR reads each page |
| Demo page | ✅ | Browser UI at /demo for testing |
| Health check | ✅ | GET /health returns service status |

### What's Next (Phase 3+)

- **LLM Document Understanding** — Feed OCR text to Gemini 2.5 Flash to extract structured invoice fields
- **Semantic Field Mapping** — Handle varying terminologies (e.g., "Invoice Number" vs "Bill No")
- **Docker Containerization** — Multi-stage Docker build
- **Deployment** — Railway (free), then client's preferred infra

---

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

```powershell
# Clone the repo
git clone <repo-url>
cd invoice-processor

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and set your values:

```env
APP_NAME="Invoice OCR Processor"
DEBUG=true
API_KEYS=["demo-key"]           # JSON array of valid API keys
GEMINI_API_KEY=                  # Phase 3: Your Google Gemini API key
```

---

## Running Locally

```powershell
# Activate venv (if not already)
.\.venv\Scripts\Activate.ps1

# Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Testing

**Via browser:** Open `http://localhost:8080/demo`

**Via curl:**
```powershell
# Health check
curl http://localhost:8080/health

# Process invoice
curl -X POST http://localhost:8080/api/v1/process-invoice `
  -H "X-API-Key: demo-key" `
  -F "file=@invoice.pdf"
```

**Via Swagger docs:** `http://localhost:8080/docs`

---

## API Reference

### `POST /api/v1/process-invoice`

Process an invoice document and extract text.

**Headers:**
| Header | Value | Required |
|--------|-------|----------|
| `X-API-Key` | Your API key | Yes |

**Body:** `multipart/form-data`
| Field | Type | Required |
|-------|------|----------|
| `file` | File (PDF, JPG, PNG) | Yes |

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "header": {
      "company_name": "INVOICE\nInvoice No: INV-001\n...",
      "invoice_number": "",
      "gst_number": "",
      "invoice_date": "",
      "vendor": { "name": "", "address": "", "contact": "" },
      "shipping": { "name": "", "address": "", "vessel": "", "consignee": "" },
      "total_amount": 0.0,
      "currency": "",
      "tax_info": { "tax_type": "", "tax_rate": 0.0, "tax_amount": 0.0 }
    },
    "line_items": []
  }
}
```

> **Note:** Currently the raw OCR text is returned in `company_name` (first 100 chars). Full structured field extraction will be implemented in Phase 3 with Gemini.

### `GET /health`

Returns service health status.

### `GET /demo`

Serves the browser-based test UI.

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Web Framework | FastAPI (Python) | Async, auto-docs, Pydantic validation |
| OCR Engine | EasyOCR | Deep learning OCR, clean install, good accuracy |
| PDF Processing | pypdfium2 | Fast PDF-to-image rendering |
| Image Handling | Pillow + NumPy | Image loading and array conversion |
| LLM (Phase 3) | Gemini 2.5 Flash | Free tier, excellent structured JSON output |
| Auth | X-API-Key header | Simple service-to-service auth |
| Deployment | Railway → Cloud (TBD) | Free tier for prototype, flexible for production |

---

## Notes for the .NET Team

The .NET application can call this service using `HttpClient`:

```csharp
using var client = new HttpClient();
client.BaseAddress = new Uri("https://your-service.railway.app");
client.DefaultRequestHeaders.Add("X-API-Key", "your-api-key");

var content = new MultipartFormDataContent();
content.Add(new ByteArrayContent(fileBytes), "file", "invoice.pdf");

var response = await client.PostAsync("/api/v1/process-invoice", content);
var json = await response.Content.ReadAsStringAsync();
```

For authentication reference, see `app/middleware/auth.py`. For the JSON schema reference, see `app/models/response.py`.
