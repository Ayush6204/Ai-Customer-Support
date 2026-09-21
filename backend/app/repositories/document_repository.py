from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    user_id: int,
    session_id: int,
    filename: str,
    file_path: str,
    file_type: str,
    chroma_collection: str,
    status: str = "uploaded",
):
    # print("document repository -->")
    document = Document(
        user_id=user_id,
        session_id=session_id,
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        chroma_collection=chroma_collection,
        status=status,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def get_user_documents(db: Session, user_id: int):
    """
    Return only documents owned by current user.
    """

    return db.query(Document).filter(
        Document.user_id == user_id
    ).order_by(
        Document.created_at.desc()
    ).all()
    
    
def get_user_session_documents(
    db: Session,
    user_id: int,
    session_id: int
):
    """
    Return only documents that belong to current user and current session.
    This prevents Chat 2 from seeing Chat 1 documents.
    """

    return db.query(Document).filter(
        Document.user_id == user_id,
        Document.session_id == session_id
    ).order_by(
        Document.created_at.desc()
    ).all()


def get_user_document_by_id(
    db: Session,
    user_id: int,
    document_id: int
):
    """
    Return document only if it belongs to current user.
    """

    return db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()

def get_user_session_document_by_id(
    db: Session,
    user_id: int,
    session_id: int,
    document_id: int
):
    """
    Return document only if it belongs to current user and current session.
    """

    return db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id,
        Document.session_id == session_id
    ).first()

def update_document_status(
    db: Session,
    document_id: int,
    status: str,
    error_message: str | None = None,
):
    # print("document repository --> update document status")
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return None

    document.status = status
    document.error_message = error_message

    db.commit()
    db.refresh(document)

    return document


def delete_document_metadata(
    db: Session,
    user_id: int,
    document_id: int
):
    """
    Delete SQL metadata only if document belongs to current user.
    """

    document = get_user_document_by_id(
        db=db,
        user_id=user_id,
        document_id=document_id
    )

    if not document:
        return None

    db.delete(document)
    db.commit()

    return document


