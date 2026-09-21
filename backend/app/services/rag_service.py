from typing import List
from uuid import uuid4

from fastapi import HTTPException, status
from langchain_core.documents import Document as LangChainDocument
from langchain_chroma import Chroma

from app.core.config import settings
from app.services.embedding_service import get_embedding_model


def get_chroma_vectorstore(collection_name: str):
    try:
        embeddings = get_embedding_model()

        vectorstore = Chroma(
    collection_name=collection_name,
    embedding_function=get_embedding_model(),
    persist_directory=settings.CHROMA_DB_DIR,
)

        return vectorstore

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ChromaDB initialization failed: {str(e)}"
        )


def store_document_chunks_in_chromadb(
    chunks: List[str],
    user_id: int,
    session_id: int,
    document_id: int,
    filename: str,
    collection_name: str,
):
    try:
        print("rag servicves-->")
        vectorstore = get_chroma_vectorstore(collection_name)

        documents = []
        ids = []

        for index, chunk in enumerate(chunks):
            chunk_id = f"user_{user_id}_doc_{document_id}_chunk_{index}_{uuid4().hex}"

            documents.append(
                LangChainDocument(
                    page_content=chunk,
                    metadata={
                        "user_id": str(user_id),
                        "session_id": str(session_id),
                        "document_id": str(document_id),
                        "filename": filename,
                        "chunk_index": index,
                    }
                )
            )

            ids.append(chunk_id)

        vectorstore.add_documents(
            documents=documents,
            ids=ids
        )

        return {
            "total_chunks": len(documents),
            "chunk_ids": ids
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store chunks in ChromaDB: {str(e)}"
        )


def retrieve_user_chunks(
    question: str,
    user_id: int,
    session_id:int,
    collection_name: str,
    document_id: int | None = None,
    k: int = 4,
):
    # print("rag servicves (retrieve chunks)-->")
    """
    Retrieve chunks using:
    - question embedding
    - top_k relevant chunks
    - user_id metadata filter
    - optional document_id filter
    - similarity score
    """

    try:
        vectorstore = get_chroma_vectorstore(collection_name)
        # print("vectorstore initialized in rag service", vectorstore)

        if document_id is not None:
            metadata_filter = {
                "$and": [
                    {"user_id": {"$eq": str(user_id)}},
                    {"session_id": {"$eq": str(session_id)}},
                    {"document_id": {"$eq": str(document_id)}}
                ]
            }
        else:
            metadata_filter = {
                "$and": [
                    {"user_id": {"$eq": str(user_id)}},
                    {"session_id": {"$eq": str(session_id)}}
                ]
            }

        results_with_scores = vectorstore.similarity_search_with_score(
            query=question,
            k=k,
            filter=metadata_filter
        )
        # print(f"Retrieved {len(results_with_scores)} chunks from ChromaDB")

        final_results = []

        for chunk, score in results_with_scores:
            chunk.metadata["similarity_score"] = float(score)
            final_results.append(chunk)

        return final_results

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chunks from ChromaDB: {str(e)}"
        )
        
        
def delete_document_chunks_from_chromadb(
    user_id: int,
    document_id: int,
    collection_name: str,
):
    """
    Delete all ChromaDB chunks for one document.

    Important:
    Deletes only vectors matching:
    - user_id
    - document_id
    """

    try:
        vectorstore = get_chroma_vectorstore(collection_name)

        metadata_filter = {
            "$and": [
                {"user_id": {"$eq": str(user_id)}},
                {"document_id": {"$eq": str(document_id)}}
            ]
        }

        # Access underlying Chroma collection.
        vectorstore._collection.delete(
            where=metadata_filter
        )

        return {
            "message": "Document chunks deleted from ChromaDB"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document chunks from ChromaDB: {str(e)}"
        )


def delete_all_user_chunks_from_chromadb(
    user_id: int,
    collection_name: str,
):
    """
    Optional helper.
    Delete all vectors for a user from one collection.
    """

    try:
        vectorstore = get_chroma_vectorstore(collection_name)

        metadata_filter = {
            "user_id": {"$eq": str(user_id)}
        }

        vectorstore._collection.delete(
            where=metadata_filter
        )

        return {
            "message": "User chunks deleted from ChromaDB"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user chunks from ChromaDB: {str(e)}"
        )