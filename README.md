# Medical Report Visualization API

A FastAPI backend service for extracting text from medical reports using the Gemini API and parsing them into structured data with MongoDB storage.

## Features

- Extract text from various file formats (PDF, JPG, PNG, TIFF)
- Convert PDF documents to images for processing
- Parse medical reports to extract patient information and test results
- Store extraction results in MongoDB with user association
- Retrieve and manage user-specific extraction data
- Health check endpoints for API monitoring

## Requirements

- Python 3.8+
- Gemini API key
- MongoDB database

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
4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URL=your_mongodb_connection_string_here
   ```

## Running the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload false
```

```bash
python app/main.py
```

API Documentation at:

- Swagger UI: http://localhost:5000/docs
- ReDoc: https://localhost:5000/redoc

## API Endpoints

### Health & Data Management

#### GET /api/v1/health

Health check endpoint for API monitoring.

#### GET /api/v1/user/{user_id}

Retrieve all extraction results for a specific user.

#### DELETE /api/v1/user/{user_id}

Delete all extraction results for a specific user.

#### DELETE /api/v1/record/{document_id}

Delete a specific extraction result by document ID.

### Data Extraction

#### POST /api/v1/extract

Extract information from a medical report file.

**Parameters:**

- `user_id` (optional): User identifier for storing results
- `file`: Medical report file (PDF, JPG, PNG, TIFF)

**Response:**

```json
{
  "patient": {
    "name": "John Doe",
    "age": "45 Yrs",
    "gender": "M",
    "referred_by": "Dr. Smith",
    "date": "2025-05-21"
  },
  "reports": [
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

## Project Structure

```
app/
├── api/
│   ├── endpoints.py          # Main extraction endpoints
│   └── health.py            # Health check and data management
├── core/
│   └── config.py            # Application configuration
├── database/
│   └── data.py              # MongoDB operations
├── models/
│   └── schemas.py           # Pydantic data models
├── services/
│   └── gemini_service.py    # Gemini API integration
├── utils/
│   └── file_utils.py        # File handling utilities
└── main.py                  # FastAPI application entry point
```
