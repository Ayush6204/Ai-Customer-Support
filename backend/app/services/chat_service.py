from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.ownership_service import (
    validate_session_owner,
    validate_document_session_owner,
)
from app.services.rag_service import retrieve_user_chunks
from app.services.prompt_service import (
    build_rag_prompt,
    build_no_document_guard_prompt,
    build_basic_conversation_prompt,
    build_message_intent_guard_prompt,
)
from app.services.llm_service import generate_answer_from_prompt
from app.repositories.chat_repository import (
    get_recent_chat_messages,
    create_chat_message,
)
from app.repositories.document_repository import get_user_document_by_id
from app.repositories.document_repository import get_user_session_documents

from app.services.context_service import (
    build_limited_rag_context,
    has_relevant_context,
    fallback_no_context_answer,
)

def build_sources_from_chunks(chunks):
    print("chat service (build sources from chunks) -->")
    sources = []

    for chunk in chunks:
        preview = chunk.page_content[:200].replace("\n", " ")
        print("Chunk preview:", preview)

        sources.append(
            {
                "document_id": chunk.metadata.get("document_id"),
                "filename": chunk.metadata.get("filename"),
                "chunk_index": chunk.metadata.get("chunk_index"),
                "similarity_score": chunk.metadata.get("similarity_score"),
                "preview": preview,
            }
        )
    print(f"Built sources from {len(chunks)} chunks")
    return sources


def get_default_collection_name(user_id: int) -> str:
    return f"user_{user_id}_documents"

def build_contexts_from_chunks(retrieved_chunks):
    """
    Convert retrieved ChromaDB chunks into RAGAS-compatible contexts.

    RAGAS expects:
    contexts = [
        "full chunk text 1",
        "full chunk text 2"
    ]
    """

    contexts = []

    for chunk in retrieved_chunks:
        if isinstance(chunk, dict):
            text = (
                chunk.get("page_content")
                or chunk.get("content")
                or chunk.get("text")
                or chunk.get("document")
                or chunk.get("preview")
                or ""
            )
        else:
            text = (
                getattr(chunk, "page_content", None)
                or getattr(chunk, "content", None)
                or getattr(chunk, "text", None)
                or getattr(chunk, "document", None)
                or ""
            )

        if text and text.strip():
            contexts.append(text.strip())

    return contexts

def check_session_document_status(
    db: Session,
    user_id: int,
    session_id: int
):
    documents = get_user_session_documents(
        db=db,
        user_id=user_id,
        session_id=session_id
    )

    if not documents:
        return {
            "status": "no_documents",
            "documents": []
        }

    processing_documents = [
        document for document in documents
        if document.status in ["uploaded", "processing"]
    ]

    if processing_documents:
        return {
            "status": "processing",
            "documents": processing_documents
        }

    completed_documents = [
        document for document in documents
        if document.status == "completed"
    ]

    if completed_documents:
        return {
            "status": "completed",
            "documents": completed_documents
        }

    return {
        "status": "failed",
        "documents": documents
    }


def answer_without_completed_document(
    db: Session,
    current_user,
    session_id: int,
    question: str,
    document_status: str,
    document_id: int | None = None,
):
    """
    Used when no completed document context is available.

    The LLM is allowed to answer greetings/basic conversation,
    but must refuse knowledge-based questions based on the guard prompt.
    """

    prompt = build_no_document_guard_prompt(
        current_question=question,
        session_document_status=document_status
    )

    answer = generate_answer_from_prompt(prompt)

    message = create_chat_message(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        document_id=document_id,
        question=question,
        answer=answer,
        sources=[]
    )

    return {
        "answer": answer,
        "sources": [],
        "contexts": [],
        "session_id": session_id,
        "timestamp": message.created_at or datetime.now(timezone.utc),
    }    
    
    
def is_basic_conversation_message(question: str) -> bool:
    """
    Uses LLM to decide if message is greeting/basic conversation.
    If the guard fails, default to RAG for safety.
    """

    prompt = build_message_intent_guard_prompt(question)

    result = generate_answer_from_prompt(prompt)

    normalized = result.strip().upper()

    return "BASIC_CONVERSATION" in normalized and "DOCUMENT_OR_KNOWLEDGE_QUESTION" not in normalized


def answer_basic_conversation(
    db: Session,
    current_user,
    session_id: int,
    question: str,
):
    prompt = build_basic_conversation_prompt(question)

    answer = generate_answer_from_prompt(prompt)

    message = create_chat_message(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        document_id=None,
        question=question,
        answer=answer,
        sources=[]
    )

    return {
        "answer": answer,
        "sources": [],
        "contexts": [],
        "session_id": session_id,
        "timestamp": message.created_at or datetime.now(timezone.utc),
    }
    

def ask_question_service(
    db: Session,
    current_user,
    session_id: int,
    question: str,
    document_id: int | None = None,
):
    """
    Full RAG question-answering flow.

    Cases:
    1. No document uploaded:
       - allow greeting/basic conversation using guard prompt
       - block knowledge questions

    2. Document processing:
       - allow greeting/basic conversation using guard prompt
       - tell user document is processing for document/knowledge questions

    3. Document failed:
       - tell user to reprocess/upload again

    4. Document completed:
       - retrieve chunks from ChromaDB
       - build RAG prompt
       - generate answer
       - save message
    """

    session = validate_session_owner(
        db=db,
        session_id=session_id,
        current_user_id=current_user.id
    )
    
    if is_basic_conversation_message(question):
        return answer_basic_conversation(
            db=db,
            current_user=current_user,
            session_id=session.id,
            question=question
        )

    collection_name = get_default_collection_name(current_user.id)

    # ======================================================
    # CASE 1: User selected a specific document
    # ======================================================
    if document_id is not None:
        document = validate_document_session_owner(
            db=db,
            document_id=document_id,
            session_id=session.id,
            current_user_id=current_user.id
        )

        if document.status in ["uploaded", "processing"]:
            return answer_without_completed_document(
                db=db,
                current_user=current_user,
                session_id=session.id,
                question=question,
                document_status="processing",
                document_id=document.id,
            )

        if document.status == "failed":
            return answer_without_completed_document(
                db=db,
                current_user=current_user,
                session_id=session.id,
                question=question,
                document_status="failed",
                document_id=document.id,
            )

        collection_name = document.chroma_collection

    # ======================================================
    # CASE 2: User did not select a specific document
    # Check current session document status.
    # ======================================================
    if document_id is None:
        document_status = check_session_document_status(
            db=db,
            user_id=current_user.id,
            session_id=session.id
        )

        if document_status["status"] in ["no_documents", "processing", "failed"]:
            return answer_without_completed_document(
                db=db,
                current_user=current_user,
                session_id=session.id,
                question=question,
                document_status=document_status["status"],
                document_id=None,
            )

    # ======================================================
    # CASE 3: Completed document exists, normal RAG flow
    # ======================================================
    retrieved_chunks = retrieve_user_chunks(
        question=question,
        user_id=current_user.id,
        session_id=session.id,
        collection_name=collection_name,
        document_id=document_id,
        k=settings.RAG_TOP_K
    )

    recent_history = get_recent_chat_messages(
        db=db,
        user_id=current_user.id,
        session_id=session.id,
        limit=settings.MAX_HISTORY_MESSAGES
    )

    # RAGAS contexts
    contexts = build_contexts_from_chunks(retrieved_chunks)

    if not has_relevant_context(retrieved_chunks):
        answer = fallback_no_context_answer()
        sources = []
    else:
        limited_context = build_limited_rag_context(
            chunks=retrieved_chunks,
            recent_messages=recent_history,
            current_question=question,
            max_document_context_chars=settings.MAX_DOCUMENT_CONTEXT_CHARS,
            max_history_context_chars=settings.MAX_HISTORY_CONTEXT_CHARS,
            max_question_chars=settings.MAX_QUESTION_CHARS,
        )

        prompt = build_rag_prompt(
            document_context=limited_context["document_context"],
            history_context=limited_context["history_context"],
            current_question=limited_context["current_question"],
        )

        answer = generate_answer_from_prompt(prompt)

        sources = build_sources_from_chunks(retrieved_chunks)

    message = create_chat_message(
        db=db,
        user_id=current_user.id,
        session_id=session.id,
        document_id=document_id,
        question=question,
        answer=answer,
        sources=sources
    )

    return {
        "answer": answer,
        "sources": sources,
        "contexts": contexts,
        "session_id": session.id,
        "timestamp": message.created_at or datetime.now(timezone.utc),
    }    
    
    
def check_session_document_status(
    db: Session,
    user_id: int,
    session_id: int
):
    """
    Check documents inside current chat session.

    Returns:
    - no_documents
    - processing
    - failed
    - completed
    """

    documents = get_user_session_documents(
        db=db,
        user_id=user_id,
        session_id=session_id
    )

    if not documents:
        return {
            "status": "no_documents",
            "documents": []
        }

    processing_docs = [
        doc for doc in documents
        if doc.status in ["uploaded", "processing"]
    ]

    if processing_docs:
        return {
            "status": "processing",
            "documents": processing_docs
        }

    completed_docs = [
        doc for doc in documents
        if doc.status == "completed"
    ]

    if completed_docs:
        return {
            "status": "completed",
            "documents": completed_docs
        }

    return {
        "status": "failed",
        "documents": documents
    }
    
    
    
    
    
    
