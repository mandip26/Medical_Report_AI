from services.gemini_service import GeminiService
import os
import re
import json
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from utils.file_utils import save_uploaded_file, remove_file
import dotenv
from database.data import save_extraction_result

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
    user_id: str = None,
    file: UploadFile = File(...),
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".jpg", ".jpeg", ".png", ".tiff"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = save_uploaded_file(file, ext)      
    try:
        results = gemini_service.extract_from_file(file_path, ext, PROMPT)
        clean_responses = []
        for result in results:
            cleaned_result = re.sub(r'^```json\s*|\s*```', "", result)
            clean_responses.append(json.loads(cleaned_result))
        
        # Consolidate multi-page results
        if len(clean_responses) == 1:
            consolidated_response = clean_responses[0]
        else:
            # Take patient info from first page
            consolidated_response = {
                "patient": clean_responses[0]["patient"],
                "reports": []
            }
            # Combine all reports from all pages
            for page_response in clean_responses:
                consolidated_response["reports"].extend(page_response["reports"])
        
        # Store in database if user_id is provided
        if user_id:
            save_extraction_result(user_id, consolidated_response)
        
        return consolidated_response
    finally:
        remove_file(file_path)
