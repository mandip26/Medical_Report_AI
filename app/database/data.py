import pymongo
import sys
import os
import dotenv
from bson import ObjectId

dotenv.load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

try:
    client = pymongo.MongoClient(MONGODB_URL)
except pymongo.errors.ConfigurationError as e:
    print(f"Failed to connect to MongoDB: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize database and collection
db = client.get_database("blood_donation_db")
extraction_collection = db.get_collection("user_report_data")

def save_extraction_result(user_id: str, extraction_result: dict):
    """
    Save extraction results to MongoDB
    
    Args:
        user_id: Unique identifier for the user
        extraction_result: The extraction result data to be saved
        
    Returns:
        The inserted document's ID
    """
    document = {
        "user_id": user_id,
        "extraction_result": extraction_result
    }
    
    result = extraction_collection.insert_one(document)
    return result.inserted_id

def get_extraction_results_by_user_id(user_id: str):
    """
    Retrieve extraction results for a specific user
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        List of extraction results for the user with document IDs
    """
    results = list(extraction_collection.find({"user_id": user_id}))
    # Convert ObjectId to string for JSON serialization
    for result in results:
        result["_id"] = str(result["_id"])
    return results

def delete_extraction_results_by_user_id(user_id: str):
    """
    Delete all extraction results for a specific user
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Number of deleted documents
    """
    result = extraction_collection.delete_many({"user_id": user_id})
    return result.deleted_count

def delete_extraction_result_by_id(document_id: str):
    """
    Delete a specific extraction result by document ID
    
    Args:
        document_id: The MongoDB document ID
        
    Returns:
        Number of deleted documents (0 or 1)
    """
    try:
        result = extraction_collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count
    except Exception:
        return 0
