from typing import List

from langchain_core.documents import Document as LangChainDocument

from app.models.chat_message import ChatMessage


def build_document_context(
    chunks: List[LangChainDocument],
    max_chars_per_chunk: int = 1200
) -> str:
    print("context service (build document context) -->")
    """
    Convert retrieved ChromaDB chunks into clean context text.
    """

    if not chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        filename = chunk.metadata.get("filename", "unknown")
        document_id = chunk.metadata.get("document_id", "unknown")
        chunk_index = chunk.metadata.get("chunk_index", "unknown")

        content = chunk.page_content.strip()

        if len(content) > max_chars_per_chunk:
            content = content[:max_chars_per_chunk] + "..."

        context_parts.append(
            f"""
[Document Context {index}]
Filename: {filename}
Document ID: {document_id}
Chunk Index: {chunk_index}

{content}
"""
        )
    print(f"Built document context with {len(context_parts)} parts")

    return "\n".join(context_parts).strip()


def build_recent_history_context(
    messages: List[ChatMessage],
    max_chars_per_message: int = 600
) -> str:
    print("context service (build recent history context) -->")
    """
    Convert recent chat history into compact context.
    Do not send full history.
    """

    if not messages:
        return ""

    history_parts = []

    for message in messages:
        question = message.question.strip()
        answer = message.answer.strip()

        if len(question) > max_chars_per_message:
            question = question[:max_chars_per_message] + "..."

        if len(answer) > max_chars_per_message:
            answer = answer[:max_chars_per_message] + "..."

        history_parts.append(
            f"""
User: {question}
Assistant: {answer}
"""
        )
    print(f"Built history context with {len(history_parts)} parts")
    return "\n".join(history_parts).strip()


def build_rag_context(
    chunks: List[LangChainDocument],
    recent_messages: List[ChatMessage],
    current_question: str,
) -> dict:
    # print("context service (build rag context) -->")
    """
    Combine:
    - Relevant document chunks
    - Recent chat history
    - Current question
    """

    document_context = build_document_context(chunks)
    # print(f"Document context length: {len(document_context)} characters")
    history_context = build_recent_history_context(recent_messages)
    # print(f"History context length: {len(history_context)} characters")

    return {
        "document_context": document_context,
        "history_context": history_context,
        "current_question": current_question.strip(),
    }
    

def trim_text_to_limit(text: str, max_chars: int) -> str:
    # print("context service (trim text to limit) -->")
    """
    Simple token-safe strategy using character limit.
    Later you can replace this with token counting using tiktoken.
    """

    if not text:
        return ""

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n...[trimmed due to context limit]"


def apply_context_limits(
    document_context: str,
    history_context: str,
    question: str,
    max_document_context_chars: int = 5000,
    max_history_context_chars: int = 2000,
    max_question_chars: int = 1000,
) -> dict:
    # print("context service (apply context limits) -->")
    """
    Limit context before sending to LLM.

    Strategy:
    - Limit document chunks context
    - Limit recent history
    - Limit current question
    """

    limited_document_context = trim_text_to_limit(
        document_context,
        max_document_context_chars
    )
    # print(f"Limited document context length: {len(limited_document_context)} characters")
    limited_history_context = trim_text_to_limit(
        history_context,
        max_history_context_chars
    )
    # print(f"Limited history context length: {len(limited_history_context)} characters")
    # print(f"History context length: {len(history_context)} characters")
    limited_question = trim_text_to_limit(
        question,
        max_question_chars
    )
    # print(f"Limited question length: {len(limited_question)} characters")
    return {
        "document_context": limited_document_context,
        "history_context": limited_history_context,
        "current_question": limited_question,
    }


def build_limited_rag_context(
    chunks: List[LangChainDocument],
    recent_messages: List[ChatMessage],
    current_question: str,
    max_document_context_chars: int = 5000,
    max_history_context_chars: int = 2000,
    max_question_chars: int = 1000,
) -> dict:
    # print("context service (build limited context) -->")
    """
    Final context builder used before prompt creation.
    """

    raw_context = build_rag_context(
        chunks=chunks,
        recent_messages=recent_messages,
        current_question=current_question,
    )
    # print("raw context", raw_context)

    limited_context = apply_context_limits(
        document_context=raw_context["document_context"],
        history_context=raw_context["history_context"],
        question=raw_context["current_question"],
        max_document_context_chars=max_document_context_chars,
        max_history_context_chars=max_history_context_chars,
        max_question_chars=max_question_chars,
    )
    # print("limited context", limited_context)
    return limited_context

def has_relevant_context(chunks: List[LangChainDocument]) -> bool:
    """
    Check whether retrieval returned usable chunks.
    """

    if not chunks:
        return False

    for chunk in chunks:
        if chunk.page_content and chunk.page_content.strip():
            return True

    return False


def fallback_no_context_answer() -> str:
    return "I could not find this information in this chat session's uploaded documents."