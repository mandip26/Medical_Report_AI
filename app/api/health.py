from fastapi import APIRouter, HTTPException
from database.data import get_extraction_results_by_user_id, delete_extraction_results_by_user_id, delete_extraction_result_by_id

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the API
    Returns a simple status for API connectivity tests
    """
    return {"status": "ok", "message": "API is running"}

@router.get("/user/{user_id}")
async def get_user_data(user_id: str):
    """
    Retrieve extraction results for a specific user
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        List of extraction results for the user
    """
    results = get_extraction_results_by_user_id(user_id)
    if not results:
        return {"message": "No data found for this user ID"}
    return results

@router.delete("/user/{user_id}")
async def delete_user_data(user_id: str):
    """
    Delete all extraction results for a specific user
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Confirmation message with number of deleted records
    """
    deleted_count = delete_extraction_results_by_user_id(user_id)
    if deleted_count == 0:
        return {"message": "No data found for this user ID"}
    return {"message": f"Successfully deleted {deleted_count} records for user {user_id}"}

@router.delete("/record/{document_id}")
async def delete_individual_record(document_id: str):
    """
    Delete a specific extraction result by document ID
    
    Args:
        document_id: The MongoDB document ID
        
    Returns:
        Confirmation message
    """
    deleted_count = delete_extraction_result_by_id(document_id)
    if deleted_count == 0:
        return {"message": "Record not found or invalid ID"}
    return {"message": "Record successfully deleted"}
