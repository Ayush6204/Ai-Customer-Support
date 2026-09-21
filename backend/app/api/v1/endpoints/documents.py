from fastapi import APIRouter, Depends, UploadFile, File, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import require_user
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import (
    upload_and_process_document,
    list_my_documents,
    get_my_document,
    delete_my_document,
    reprocess_my_document,
)


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_document(
    session_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    # print("endpoint-->")
    return await upload_and_process_document(
        db=db,
        file=file,
        current_user=current_user,
        session_id=session_id,
        background_tasks=background_tasks
    )

@router.get(
    "",
    response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    """
    Task 61:
    Return only current user's documents.
    """

    return list_my_documents(
        db=db,
        current_user=current_user
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    """
    Task 62:
    Validate ownership and return single document.
    """

    return get_my_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )


@router.delete(
    "/{document_id}"
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    """
    Task 63:
    Validate ownership.
    Delete SQL metadata.
    Delete uploaded file.
    Delete related ChromaDB chunks.
    """

    return delete_my_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )


@router.post(
    "/{document_id}/reprocess",
    response_model=DocumentResponse
)
def reprocess_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_user),
):
    """
    Task 64:
    Validate ownership.
    Delete old vectors.
    Extract text again.
    Create new chunks.
    Store new vectors.
    """

    return reprocess_my_document(
        db=db,
        current_user=current_user,
        document_id=document_id
    )