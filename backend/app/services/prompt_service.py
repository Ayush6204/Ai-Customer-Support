from typing import List

from langchain_core.documents import Document as LangChainDocument

from app.models.chat_message import ChatMessage


def format_context(chunks: List[LangChainDocument]) -> str:
    if not chunks:
        return "No relevant context found."

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        filename = chunk.metadata.get("filename", "unknown")
        chunk_index = chunk.metadata.get("chunk_index", "unknown")

        context_parts.append(
            f"""
[Context {index}]
Source File: {filename}
Chunk Index: {chunk_index}
Content:
{chunk.page_content}
"""
        )

    return "\n".join(context_parts)


def format_chat_history(messages: List[ChatMessage]) -> str:
    if not messages:
        return "No previous chat history."

    history_parts = []

    for message in messages:
        history_parts.append(
            f"""
User: {message.question}
Assistant: {message.answer}
"""
        )

    return "\n".join(history_parts)


def build_rag_prompt(
    document_context: str,
    history_context: str,
    current_question: str,
) -> str:
    print("prompt service (build rag prompt) -->")
    prompt = f"""
You are a helpful RAG assistant.

SYSTEM INSTRUCTION:
Answer the user's question using only the uploaded document context provided below.
Do not use outside knowledge.
Be clear, simple, and accurate.

SAFETY RULE:
If the answer is not available in the retrieved document context, say:
"I could not find this information in your uploaded documents."

RETRIEVED DOCUMENT CONTEXT:
{document_context if document_context else "No relevant document context found."}

RECENT CHAT HISTORY:
{history_context if history_context else "No recent chat history."}

CURRENT USER QUESTION:
{current_question}

ANSWER FORMATTING RULE:
- Give a direct answer first.
- Use bullet points if helpful.
- Mention source filenames when useful.
- Do not invent facts.
- If context is insufficient, say you could not find it in uploaded documents.

FINAL ANSWER:
"""
    print("Built raw prompt:",prompt.strip())
    return prompt.strip()


def build_no_document_guard_prompt(
    current_question: str,
    session_document_status: str
) -> str:
    return f"""
You are a document-based RAG assistant.

CURRENT CHAT SESSION DOCUMENT STATUS:
{session_document_status}

USER MESSAGE:
{current_question}

VERY IMPORTANT RULES:
1. You may reply naturally ONLY if the user message is greeting, small talk, thanks, or asking about how to use this app.
2. If the user asks any knowledge-based question, factual question, explanation, definition, recipe, coding question, summary, document question, or general information question, you must NOT answer from your own knowledge.
3. If no completed document is available, tell the user that you can answer only after they upload a document in this chat session.
4. If the document is processing, tell the user that the document is still processing and they should try again after processing is completed.
5. Do not invent document content.
6. Do not answer using outside knowledge.
7. Keep the answer short and clear.

# Allowed examples:
# User: hi
# Assistant: Hello! How can I help you with your documents today?

# User: hello
# Assistant: Hi! Upload a document in this chat session and I can answer questions from it.

# User: how are you?
# Assistant: I am ready to help you with your uploaded documents.

# User: what can you do?
# Assistant: I can answer questions from documents uploaded in this chat session.

# Blocked examples:
# User: what is machine learning?
# Assistant: I could not find this information in this chat session's uploaded documents.

# User: explain Python list
# Assistant: I could not find this information in this chat session's uploaded documents.

FINAL ANSWER:
""".strip()


def build_message_intent_guard_prompt(current_question: str) -> str:
    return f"""
You are an intent classifier for a document-based RAG chatbot.

USER MESSAGE:
{current_question}

Your job is to classify the user message into exactly one category.

Return only one of these two labels:
BASIC_CONVERSATION
DOCUMENT_OR_KNOWLEDGE_QUESTION

CATEGORY 1: BASIC_CONVERSATION

Use BASIC_CONVERSATION if the user message is:
- greeting
- small talk
- thanks
- goodbye
- asking who you are
- asking your name
- asking about yourself
- asking what you can do
- asking how to use the app
- asking whether you can help

Examples of BASIC_CONVERSATION:
- hi
- hello
- hey
- good morning
- how are you?
- thanks
- thank you
- bye
- who are you?
- what are you?
- what is your name?
- what your name?
- your name?
- can you tell me about yourself?
- tell me about yourself
- what can you do?
- what you do?
- how can you help me?
- how to use this app?
- can you help me?

CATEGORY 2: DOCUMENT_OR_KNOWLEDGE_QUESTION

Use DOCUMENT_OR_KNOWLEDGE_QUESTION if the user asks for:
- factual information
- explanation
- definition
- summary
- recipe
- coding help
- document content
- document summary
- comparison
- analysis
- general knowledge
- anything that needs uploaded document context or outside knowledge

Examples of DOCUMENT_OR_KNOWLEDGE_QUESTION:
- what is machine learning?
- what is sunlight?
- explain this document
- summarize the PDF
- give me the summary of this document
- what is the conclusion?
- give me pizza recipe
- explain Python list
- what dataset is used?
- tell me about the project
- what is artificial intelligence?

IMPORTANT:
If the message contains both a greeting and a real knowledge/document question, classify it as DOCUMENT_OR_KNOWLEDGE_QUESTION.

Examples:
- hi, what is this document about?
- hello, explain this PDF
- hey, what dataset is used?
- hi, what is machine learning?

Return only the label.
Do not explain.
Do not add punctuation.
""".strip()


def build_basic_conversation_prompt(current_question: str) -> str:
    return f"""
You are a friendly document-based RAG assistant.

USER MESSAGE:
{current_question}

Rules:
1. Reply naturally and briefly.
2. You may answer greetings, small talk, thanks, goodbye, who you are, your name, what you can do, and how to use the app.
3. You must not answer factual knowledge questions here.
4. You must not pretend you read a document unless document context is provided.
5. Keep the response short.

Your identity:
You are a document-based RAG assistant.
You help users upload documents and ask questions from documents uploaded in the current chat session.

If the user asks your name or who you are, say you are their document assistant.
If the user asks what you can do, say you can answer questions from documents uploaded in this chat session.

FINAL ANSWER:
""".strip()


def build_basic_conversation_prompt(current_question: str) -> str:
    return f"""
You are a friendly document-based RAG assistant.

USER MESSAGE:
{current_question}

Rules:
1. Reply naturally and briefly.
2. You may greet the user, respond to small talk, thanks, goodbye, or explain what you can do.
3. Do not answer factual knowledge questions here.
4. Do not pretend you read a document unless document context is provided.
5. Keep response short.

If user asks what you can do, explain:
"I can answer questions from documents uploaded in this chat session."

FINAL ANSWER:
""".strip()