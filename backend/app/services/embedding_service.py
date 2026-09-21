from typing import List

from fastapi import HTTPException, status
from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class HuggingFaceBGEEmbeddings:
    """
    LangChain-compatible embedding wrapper for Hugging Face Inference API.

    Chroma expects an object with:
    - embed_documents(texts: list[str]) -> list[list[float]]
    - embed_query(text: str) -> list[float]
    """

    def __init__(self):
        if not settings.HF_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="HF_TOKEN is missing. Add it in your .env file."
            )

        self.client = InferenceClient(
            provider=settings.HF_EMBEDDING_PROVIDER,
            api_key=settings.HF_TOKEN,
        )

        self.model = settings.HF_EMBEDDING_MODEL

    def _normalize_embedding_response(self, response):
        """
        Hugging Face providers may return:
        - list[float]
        - list[list[float]]
        - object with .tolist()
        This function normalizes response into Python lists.
        """

        if hasattr(response, "tolist"):
            response = response.tolist()

        return response

    def embed_query(self, text: str) -> List[float]:
        try:
            response = self.client.feature_extraction(
                text,
                model=self.model,
            )

            response = self._normalize_embedding_response(response)

            # Sometimes response is [[...]], sometimes [...]
            if response and isinstance(response[0], list):
                return response[0]

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Hugging Face query embedding failed: {str(e)}"
            )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            embeddings = []

            for text in texts:
                response = self.client.feature_extraction(
                    text,
                    model=self.model,
                )

                response = self._normalize_embedding_response(response)

                if response and isinstance(response[0], list):
                    embeddings.append(response[0])
                else:
                    embeddings.append(response)

            return embeddings

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Hugging Face document embedding failed: {str(e)}"
            )


def get_embedding_model():
    """
    Main embedding model used by ChromaDB.
    """

    if settings.EMBEDDING_PROVIDER == "huggingface":
        return HuggingFaceBGEEmbeddings()

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="No valid embedding provider configured."
    )


def test_embedding_model(text: str):
    embeddings = get_embedding_model()
    vector = embeddings.embed_query(text)

    return vector

# class LocalBGEEmbeddings:
#     """
#     LangChain-compatible local embedding wrapper.

#     Chroma expects:
#     - embed_documents(texts) -> list[list[float]]
#     - embed_query(text) -> list[float]
#     """

#     def __init__(self):
#         try:
#             self.model = SentenceTransformer(settings.HF_EMBEDDING_MODEL)
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Local embedding model loading failed: {str(e)}"
#             )

#     def embed_query(self, text: str) -> List[float]:
#         try:
#             embedding = self.model.encode(
#                 text,
#                 normalize_embeddings=True
#             )
#             return embedding.tolist()
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Local query embedding failed: {str(e)}"
#             )

#     def embed_documents(self, texts: List[str]) -> List[List[float]]:
#         try:
#             embeddings = self.model.encode(
#                 texts,
#                 normalize_embeddings=True,
#                 batch_size=8
#             )
#             return embeddings.tolist()
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Local document embedding failed: {str(e)}"
#             )


# def get_embedding_model():
#     if settings.EMBEDDING_PROVIDER == "local_huggingface":
#         return LocalBGEEmbeddings()

#     raise HTTPException(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         detail="No valid embedding provider configured."
#     )


# def test_embedding_model(text: str):
#     embeddings = get_embedding_model()
#     return embeddings.embed_query(text)