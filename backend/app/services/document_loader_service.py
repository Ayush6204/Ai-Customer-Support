from fastapi import HTTPException, status
from pypdf import PdfReader
import docx2txt


def load_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF file is corrupted or cannot be read"
        )


def load_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TXT file is corrupted or cannot be read"
        )


def load_docx(file_path: str) -> str:
    try:
        text = docx2txt.process(file_path)
        return text or ""

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DOCX file is corrupted or cannot be read"
        )


def extract_text_from_document(file_path: str, file_type: str) -> str:
    print("document loader service --> extract text from document")
    if file_type == ".pdf":
        text = load_pdf(file_path)
        # print("======================================================")
        # print(text)

    elif file_type == ".txt":
        text = load_txt(file_path)

    elif file_type == ".docx":
        text = load_docx(file_path)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type for text extraction: {file_type}"
        )

    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document is empty or no readable text found"
        )

    return text