from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RAG Application Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql://postgres:%40Ayush321@localhost:5432/rag_db"

    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    GOOGLE_API_KEY: str = ""

    UPLOAD_DIR: str = "uploads"
    CHROMA_DB_DIR: str = "chroma_db"

    ALLOWED_FILE_TYPES: str = ".pdf,.txt,.csv,.docx,.xlsx"
    MAX_FILE_SIZE_MB: int = 10

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    EMBEDDING_PROVIDER: str = "huggingface"
    HF_EMBEDDING_MODEL: str = "BAAI/bge-m3"
    HF_EMBEDDING_PROVIDER: str = "auto"
    
    # Model Providers Configuration
    LLM_PROVIDER: str = "gemini"  # Options: "gemini" or "huggingface"
    
    # Gemini Configuration
    GEMINI_LLM_MODEL: str = "gemini-3.6-flash"  # Active stable model endpoint
    
    # Hugging Face Configuration
    HF_TOKEN: str = ""
    HF_LLM_MODEL: str = "meta-llama/Llama-3.2-1B-Instruct"
    HF_INFERENCE_PROVIDER: str = "novita"

    LLM_MAX_TOKENS: int = 512
    LLM_TEMPERATURE: float = 0.2
    
    RAG_TOP_K: int = 4
    MAX_HISTORY_MESSAGES: int = 6
    
    MAX_DOCUMENT_CONTEXT_CHARS: int = 5000
    MAX_HISTORY_CONTEXT_CHARS: int = 2000
    MAX_QUESTION_CHARS: int = 1000

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_file_types_list(self) -> List[str]:
        return [file_type.strip() for file_type in self.ALLOWED_FILE_TYPES.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Permits extra env variables without throwing validation errors


settings = Settings()