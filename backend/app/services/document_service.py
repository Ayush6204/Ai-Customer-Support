from fastapi import UploadFile, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.repositories.document_repository import (
    create_document,
    update_document_status,
    get_user_documents,
    get_user_session_documents,
    get_user_document_by_id,
    delete_document_metadata,
)
from app.services.file_storage_service import (
    save_upload_file_safely,
    delete_uploaded_file,
)
from app.services.document_loader_service import extract_text_from_document
from app.services.text_cleaning_service import clean_text
from app.services.text_splitter_service import split_text_into_chunks
from app.services.rag_service import (
    store_document_chunks_in_chromadb,
    delete_document_chunks_from_chromadb,
)
from app.services.ownership_service import validate_session_owner
from app.db.database import SessionLocal
from app.repositories.user_repository import get_user_by_id


async def upload_and_process_document(
    db: Session,
    file: UploadFile,
    current_user,
    session_id: int,
    background_tasks: BackgroundTasks
):
    # print("document service-->")
    """
    Upload and process new document inside a specific chat session.
    """

    session = validate_session_owner(
        db=db,
        session_id=session_id,
        current_user_id=current_user.id
    )

    saved_file = await save_upload_file_safely(
        file=file,
        user_id=current_user.id
    )

    collection_name = f"user_{current_user.id}_documents"
    # print(f"Collection name: {collection_name}")

    document = create_document(
        db=db,
        user_id=current_user.id,
        session_id=session.id,
        filename=saved_file["original_filename"],
        file_path=saved_file["file_path"],
        file_type=saved_file["file_type"],
        chroma_collection=collection_name,
        status="uploaded",
    )

    background_tasks.add_task(
        process_document_background,
        document_id=document.id,
        user_id=current_user.id
    )

    return document


def process_document_background(
    document_id: int,
    user_id: int
):
    """
    Background document processing.

    Important:
    Background tasks must use their own DB session.
    Do not reuse request db session here.
    """

    db = SessionLocal()

    try:
        user = get_user_by_id(
            db=db,
            user_id=user_id
        )

        document = get_user_document_by_id(
            db=db,
            user_id=user_id,
            document_id=document_id
        )

        if not user or not document:
            return

        process_existing_document(
            db=db,
            current_user=user,
            document=document
        )

    except HTTPException as e:
        update_document_status(
            db=db,
            document_id=document_id,
            status="failed",
            error_message=str(e.detail)
        )

    except Exception as e:
        update_document_status(
            db=db,
            document_id=document_id,
            status="failed",
            error_message=str(e)
        )

    finally:
        db.close()


def process_existing_document(
    db: Session,
    current_user,
    document,
):
    # print("document service --> process existing document")
    """
    Process already saved document:
    - status processing
    - extract text
    - clean text
    - split chunks
    - store chunks in ChromaDB
    - status completed
    """

    update_document_status(
        db=db,
        document_id=document.id,
        status="processing",
        error_message=None
    )

    extracted_text = extract_text_from_document(
        file_path=document.file_path,
        file_type=document.file_type
    )

    cleaned_text = clean_text(extracted_text)
    # print(f"Cleaned text: {cleaned_text[:500]}")  # Print first 500 characters of cleaned text

    if not cleaned_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document has no clean readable text"
        )

    chunks = split_text_into_chunks(
        text=cleaned_text,
        chunk_size=1000,
        chunk_overlap=200
    )
    # print(f"Number of chunks created: {len(chunks)}")
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document could not be split into chunks"
        )

    store_document_chunks_in_chromadb(
        chunks=chunks,
        user_id=current_user.id,
        session_id=document.session_id,
        document_id=document.id,
        filename=document.filename,
        collection_name=document.chroma_collection
    )
    print("Chunks stored in ChromaDB")

    update_document_status(
        db=db,
        document_id=document.id,
        status="completed",
        error_message=None
    )


def list_my_documents(db: Session, current_user):
    """
    Task 61:
    Return only current user documents.
    """

    return get_user_documents(
        db=db,
        user_id=current_user.id
    )


def get_my_document(
    db: Session,
    current_user,
    document_id: int
):
    """
    Task 62:
    Validate ownership and return document.
    """

    document = get_user_document_by_id(
        db=db,
        user_id=current_user.id,
        document_id=document_id
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document


def delete_my_document(
    db: Session,
    current_user,
    document_id: int
):
    """
    Task 63:
    Validate ownership.
    Delete ChromaDB chunks.
    Delete uploaded file.
    Delete SQL metadata.
    """

    document = get_my_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )

    # 1. Delete ChromaDB chunks first
    delete_document_chunks_from_chromadb(
        user_id=current_user.id,
        document_id=document.id,
        collection_name=document.chroma_collection
    )

    # 2. Delete uploaded file
    delete_uploaded_file(document.file_path)

    # 3. Delete SQL metadata
    delete_document_metadata(
        db=db,
        user_id=current_user.id,
        document_id=document.id
    )

    return {
        "message": "Document deleted successfully"
    }


def reprocess_my_document(
    db: Session,
    current_user,
    document_id: int
):
    """
    Task 64:
    Validate ownership.
    Delete old ChromaDB vectors.
    Extract text again.
    Create new chunks.
    Store new vectors.
    """

    document = get_my_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )

    try:
        # 1. Delete old vectors
        delete_document_chunks_from_chromadb(
            user_id=current_user.id,
            document_id=document.id,
            collection_name=document.chroma_collection
        )

        # 2. Reprocess file
        process_existing_document(
            db=db,
            current_user=current_user,
            document=document
        )

        updated_document = get_user_document_by_id(
            db=db,
            user_id=current_user.id,
            document_id=document.id
        )

        return updated_document

    except HTTPException as e:
        update_document_status(
            db=db,
            document_id=document.id,
            status="failed",
            error_message=e.detail
        )
        raise e

    except Exception as e:
        update_document_status(
            db=db,
            document_id=document.id,
            status="failed",
            error_message=str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document reprocessing failed: {str(e)}"
        )