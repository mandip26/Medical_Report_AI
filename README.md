# Medical Report Visualization API

A FastAPI backend service for extracting text from medical reports using OCR and parsing them into structured data.

## Features

- Extract text from various file formats (PDF, JPG, PNG, TIFF)
- Convert PDF documents to images if they're not text-based
- Parse medical reports to extract patient information and test results
- RESTful API with OpenAPI documentation

## Requirements

- Python 3.8+
- Tesseract OCR installed on your system

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Tesseract OCR:

   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - Mac: `brew install tesseract`

5. Adjust the Tesseract path in `app/core/config.py` if needed.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

API Documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /api/v1/extract

Extract information from a medical report file.

**Request:**

- Multipart form with file upload

**Response:**

```json
{
  "patient_info": {
    "name": "John Doe",
    "age": "45 Yrs",
    "gender": "M",
    "referred_by": "Dr. Smith",
    "date": "2025-05-21"
  },
  "report_items": [
    {
      "title": "Hemoglobin",
      "result": "14.5",
      "unit": "g/dL",
      "reference": "13.0-17.0"
    },
    {
      "title": "White Blood Cell Count",
      "result": "7.5",
      "unit": "10^3/µL",
      "reference": "4.5-11.0"
    }
  ]
}
```

## Testing

Run the tests with:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=app
```
