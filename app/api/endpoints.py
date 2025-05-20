from services.gemini_service import GeminiService
import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from utils.file_utils import save_uploaded_file, remove_file
import dotenv
# Load environment variables from .env file 
dotenv.load_dotenv()

router = APIRouter()

def get_gemini_service():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    return GeminiService(api_key)

PROMPT = """
You are a medical data extraction assistant. Extract all patient information and test results from this medical report image. 
Format the output as JSON with the following structure:
{
  "patient": {
    "name": "...",
    "age": "...",
    "gender": "...",
    "referred_by": "...",
    "date": "..."
  },
  "reports": [
    {
      "title": "...",
      "result": "...",
      "unit": "...",
      "reference": "..."
    }
  ]
}
Only provide the JSON, do not add explanations.
"""

@router.post("/extract")
async def extract(
    file: UploadFile = File(...),
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".jpg", ".jpeg", ".png", ".tiff"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = save_uploaded_file(file, ext)
    try:
        results = gemini_service.extract_from_file(file_path, ext, PROMPT)
        # For single-page, results[0] is the JSON
        return results[0]
    finally:
        remove_file(file_path)
