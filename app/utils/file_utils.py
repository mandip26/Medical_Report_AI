import tempfile
import shutil
import os
from app.core.config import settings

def save_uploaded_file(upload_file, suffix):
    """
    Save an uploaded file to a temporary location and return the path
    """
    temp_dir = settings.TEMP_DIR
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=temp_dir) as temp:
        shutil.copyfileobj(upload_file.file, temp)
        return temp.name

def remove_file(path):
    """
    Safely remove a file from the filesystem
    """
    try:
        os.unlink(path)
    except Exception:
        pass