import os
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file_type(filename: str):
    # print("file storage service (validate file type) -->")
    file_ext = get_file_extension(filename)

    if file_ext not in settings.allowed_file_types_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} is not allowed"
        )
    # print(f"validated file type: {file_ext}")
    return file_ext


def validate_file_size(file_content: bytes):
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    # print(max_size_bytes)

    if len(file_content) > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size must be less than {settings.MAX_FILE_SIZE_MB} MB"
        )


def create_user_upload_dir(user_id: int) -> str:
    # print("file storage service (create user upload dir) -->")
    user_upload_dir = os.path.join(settings.UPLOAD_DIR, f"user_{user_id}")
    os.makedirs(user_upload_dir, exist_ok=True)

    # print(f"user upload directory: {user_upload_dir}")
    return user_upload_dir


def generate_safe_filename(original_filename: str) -> str:
    # print("file storage service (generate safe filename) -->")
    file_ext = get_file_extension(original_filename)

    safe_filename = f"document_{uuid4().hex}{file_ext}"
    # print(f"generated safe filename: {safe_filename}")
    return safe_filename


async def save_upload_file_safely(
    file: UploadFile,
    user_id: int
) -> dict:
    # print("file storage service-->")
    """
    Secure file saving:
    - Validate extension
    - Validate size
    - Rename file using UUID
    - Store inside user-specific folder
    - Do not trust original filename directly
    """

    file_ext = validate_file_type(file.filename)

    file_content = await file.read()
    # print(f"file size in bytes: {len(file_content)}")

    validate_file_size(file_content)

    user_upload_dir = create_user_upload_dir(user_id)

    safe_filename = generate_safe_filename(file.filename)

    file_path = os.path.join(user_upload_dir, safe_filename)
    # print(f"final file path: {file_path}")

    # Prevent path traversal
    safe_base_path = os.path.abspath(user_upload_dir)
    safe_final_path = os.path.abspath(file_path)

    if not safe_final_path.startswith(safe_base_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file path"
        )

    with open(safe_final_path, "wb") as buffer:
        buffer.write(file_content)

    return {
        "original_filename": file.filename,
        "saved_filename": safe_filename,
        "file_path": safe_final_path,
        "file_type": file_ext,
        "file_size": len(file_content),
    }
    

def delete_uploaded_file(file_path: str):
    """
    Delete uploaded file from disk safely.

    If file does not exist, ignore.
    """

    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        return True

    except Exception:
        return False