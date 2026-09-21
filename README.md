# RAG Application - Retrieval Augmented Generation System

## 📋 Table of Contents
- [Introduction](#introduction)
- [Description](#description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Advantages](#advantages)
- [Disadvantages](#disadvantages)
- [Limitations](#limitations)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Authentication](#authentication)
- [Contributing](#contributing)

---

## Introduction

The **RAG Application** is a full-stack web application that implements Retrieval Augmented Generation (RAG) technology. It allows users to upload documents, store them in a vector database, and ask questions that are answered using intelligent retrieval and generation capabilities. The application combines the power of modern Large Language Models (LLMs) with document retrieval to provide accurate, context-aware responses.

This system bridges the gap between static document repositories and intelligent conversational AI, enabling users to have meaningful interactions with their document collections.

---

## Description

### What is RAG?

Retrieval Augmented Generation (RAG) is a machine learning technique that combines:
1. **Retrieval**: Finding relevant documents or passages from a knowledge base
2. **Augmentation**: Enriching the query with retrieved context
3. **Generation**: Using an LLM to generate answers based on the augmented context

### Application Overview

The RAG Application provides:

- **Document Management**: Upload and manage multiple document types (PDF, TXT, CSV, DOCX, XLSX)
- **Vector Storage**: Automatic conversion of documents into vector embeddings for semantic search
- **Chat Interface**: Real-time conversational interface with chat history
- **Multi-LLM Support**: Integration with multiple language models (Google Gemini, Hugging Face models)
- **User Authentication**: Secure JWT-based authentication and authorization
- **Admin Panel**: Administrative tools for managing users and documents
- **Session Management**: Persistent chat sessions with history

### Key Components

1. **Backend**: FastAPI-based REST API with comprehensive business logic
2. **Frontend**: React-based web interface with Material-UI components
3. **Vector Database**: ChromaDB for semantic search and similarity matching
4. **Relational Database**: SQLite for storing user data, chat history, and metadata
5. **Document Processing**: Automatic parsing and chunking of uploaded documents

---

## Features

✅ **User Authentication & Authorization**
- JWT-based secure authentication
- Role-based access control (Admin, User)
- Token blacklisting for logout functionality

✅ **Document Management**
- Multi-format document upload (PDF, TXT, CSV, DOCX, XLSX)
- Automatic document chunking and embedding
- Document metadata tracking
- File size validation (up to 10MB)

✅ **Chat & Conversation**
- Interactive chat interface
- Context-aware responses using RAG
- Chat history and session management
- Conversation persistence

✅ **Vector Search**
- Semantic similarity search
- Multi-embedding model support
- Configurable context retrieval (top-k results)

✅ **Multiple LLM Providers**
- Google Gemini integration
- Hugging Face LLM support
- Configurable model parameters

✅ **Admin Features**
- User management
- Document management
- System configuration
- Evaluation reports

✅ **API Documentation**
- Auto-generated OpenAPI/Swagger documentation
- RESTful API design
- Error handling and validation

---

## Tech Stack

### Backend
- **Framework**: FastAPI (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Alembic for database versioning
- **Vector Store**: ChromaDB for embeddings and semantic search
- **Authentication**: PyJWT for JWT token management
- **LLM Integration**: LangChain, Google GenAI, Hugging Face Inference
- **Document Processing**: docx2txt, openpyxl, pdf parsing libraries
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: React 19 with Vite
- **Routing**: React Router v7
- **UI Library**: Material-UI (MUI) v9
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS, Emotion CSS-in-JS
- **Build Tool**: Vite

### Infrastructure & Tools
- **Package Management**: pip (Python), npm (Node.js)
- **Version Control**: Git
- **Environment**: Python 3.10+, Node.js 16+

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       React Frontend                         │
│                    (Vite + Material-UI)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                            │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Auth Layer  │  │  API Routes  │  │   Services   │       │
│  │   (JWT)      │  │   (V1 API)   │  │   Business   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                          │                                    │
│  ┌──────────────┐  ┌──────▼──────┐  ┌──────────────┐       │
│  │  Repositories│  │  Models     │  │  Schemas     │       │
│  │ (Data Access)│  │  (ORM)      │  │  (Pydantic)  │       │
│  └──────────────┘  └─────────────┘  └──────────────┘       │
└────────────────────┬────────────────────┬────────────────────┘
                     │                    │
          ┌──────────▼──────────┐  ┌──────▼────────────┐
          │   SQLite Database   │  │   ChromaDB        │
          │  (User, Chat,       │  │  (Embeddings,     │
          │   Documents)        │  │   Vector Search)  │
          └─────────────────────┘  └───────────────────┘
```

---

## Advantages

### 🎯 For Users
- **Accurate Responses**: Combines document context with AI, reducing hallucinations
- **Quick Information Retrieval**: Fast semantic search across large document collections
- **Context Awareness**: Responses are grounded in actual document content
- **User-Friendly Interface**: Intuitive chat-based interaction with web UI
- **Multi-Format Support**: Handle various document formats seamlessly

### 🔧 For Developers
- **Modular Architecture**: Clean separation of concerns with organized layers
- **Scalable Design**: Service-oriented architecture allows easy scaling
- **Type Safety**: Pydantic schemas and type hints throughout
- **Flexible LLM Integration**: Support for multiple LLM providers and models
- **API Documentation**: Automatic Swagger/OpenAPI documentation
- **Modern Stack**: Latest versions of popular frameworks (FastAPI, React, Vite)
- **Easy Database Migrations**: Alembic for version control of schema changes

### 💼 Business Benefits
- **Reduced Operational Costs**: Leverage existing documents without manual curation
- **Improved Customer Support**: Quick, accurate answers to user queries
- **Knowledge Management**: Centralized document repository with intelligent search
- **Compliance Ready**: Audit trail of responses with document references
- **Extensible**: Easy to add new features, LLM providers, or document types

---

## Disadvantages

### ⚠️ Technical Limitations
- **Latency**: RAG adds multiple steps (retrieval → context augmentation → generation) increasing response time
- **Context Window Limits**: Long documents may exceed LLM token limits
- **Dependency on Embeddings Quality**: Poor embeddings = poor retrieval results
- **Vector Database Size**: Large document collections increase storage and search time
- **Single-Region Deployment**: Current setup is single-node (not distributed)

### 📊 Operational Challenges
- **Hallucination Risk**: LLMs can still generate plausible but incorrect information
- **Maintenance Overhead**: Requires monitoring of multiple services (API, DB, Vector DB)
- **Cold Start Time**: First queries may be slower due to model loading
- **API Rate Limits**: Dependent on external LLM providers' rate limits
- **Cost**: Using cloud-based LLM APIs can become expensive with scale

### 🔌 Integration Issues
- **Embedding Model Size**: Large embedding models require significant memory
- **Model Dependencies**: Requires downloading large pre-trained models
- **External Service Dependencies**: Relies on Google Gemini/Hugging Face availability
- **Document Parsing Limitations**: Complex PDFs with images/tables may parse incorrectly

---

## Limitations

### 🎓 Knowledge & Content
- **Static Knowledge**: Cannot access real-time information beyond training data
- **Domain Specificity**: Performance depends on document relevance and quality
- **Language Support**: Primarily optimized for English text
- **Accuracy Bound by Documents**: Cannot answer questions beyond uploaded documents
- **No Real-Time Updates**: Document changes require re-upload and re-embedding

### ⚙️ System Limitations
- **File Size**: Maximum 10MB per file upload
- **Supported Formats**: Limited to PDF, TXT, CSV, DOCX, XLSX
- **Context Window**: Fixed token limits for responses (512 tokens default)
- **Concurrent Users**: Performance degrades with many simultaneous connections
- **Storage**: Limited by disk space for ChromaDB and SQLite

### 🔐 Security & Access
- **No End-to-End Encryption**: Data transmitted and stored without encryption
- **Single Authentication Factor**: Only username/password, no 2FA
- **Database Vulnerability**: SQLite not suitable for large-scale production
- **API Rate Limiting**: Not fully implemented, susceptible to abuse
- **No Audit Logging**: Limited tracking of user actions and data access

### 📈 Scalability
- **Single-Instance Backend**: No horizontal scaling built-in
- **SQLite Limitations**: Not suitable for high-concurrency scenarios
- **No Caching Strategy**: Every query hits databases
- **Memory Intensive**: Embedding models consume significant RAM
- **No Load Balancing**: Single point of failure

---

## Installation

### Prerequisites

Ensure you have the following installed:
- **Python** 3.10 or higher
- **Node.js** 16 or higher
- **npm** 8 or higher
- **Git**

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd rag
```

### Step 2: Backend Setup

#### Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate 
 # On Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Create .env File

Create a `.env` file in the `backend` directory with the following configuration:

```env
# App Configuration
APP_NAME=RAG Application Backend
APP_VERSION=1.0.0
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./rag_app.db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API (optional)
GOOGLE_API_KEY=your-google-api-key

# Upload Configuration
UPLOAD_DIR=uploads
CHROMA_DB_DIR=chroma_db
ALLOWED_FILE_TYPES=.pdf,.txt,.csv,.docx,.xlsx
MAX_FILE_SIZE_MB=10

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Embedding Configuration
EMBEDDING_PROVIDER=huggingface
HF_EMBEDDING_MODEL=BAAI/bge-m3
HF_EMBEDDING_PROVIDER=auto
HF_TOKEN=your-huggingface-token

# LLM Configuration
LLM_PROVIDER=huggingface
GEMINI_LLM_MODEL=gemini-1.5-flash-8b
HF_LLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
HF_INFERENCE_PROVIDER=novita

# LLM Parameters
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.2

# RAG Configuration
RAG_TOP_K=4
MAX_HISTORY_MESSAGES=6
MAX_DOCUMENT_CONTEXT_CHARS=5000
MAX_HISTORY_CONTEXT_CHARS=2000
MAX_QUESTION_CHARS=1000
```

### Step 3: Frontend Setup

#### Install Dependencies

```bash
cd ../frontend
npm install
```

### Step 4: Initialize Database

First, create the initial migration:

```bash
cd backend
alembic revision --autogenerate -m "Initial schema"
```

Then apply all database migrations:

```bash
alembic upgrade head
```

This applies all database migrations and sets up the schema.

---

## Configuration

### Backend Configuration

All configuration is managed through environment variables (see .env file above).

**Key Configuration Options:**

| Variable | Description | Default |
|----------|-------------|---------|
| `EMBEDDING_PROVIDER` | Provider for embeddings (huggingface, openai) | huggingface |
| `LLM_PROVIDER` | Provider for LLM (huggingface, gemini) | huggingface |
| `RAG_TOP_K` | Number of documents to retrieve | 4 |
| `MAX_FILE_SIZE_MB` | Maximum upload file size | 10 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | 30 |

### Frontend Configuration

Frontend configuration is primarily handled in:
- `vite.config.js` - Build configuration
- `tailwind.config.js` - Styling configuration
- `.env` files for environment-specific settings

---

## Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### Build Frontend for Production

```bash
cd frontend
npm run build
```

Output files will be in the `dist/` directory.

---

## Project Structure

```
rag/
├── backend/
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core configuration and utilities
│   │   ├── db/                # Database configuration
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── repositories/      # Data access layer
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utility functions
│   │   └── main.py            # Application entry point
│   ├── alembic/               # Database migrations
│   ├── evaluation/            # RAG evaluation reports
│   ├── chroma_db/             # ChromaDB storage
│   ├── uploads/               # User uploaded files
│   ├── requirements.txt       # Python dependencies
│   └── alembic.ini            # Alembic configuration
│
├── frontend/
│   ├── src/
│   │   ├── api/               # API client setup
│   │   ├── auth/              # Authentication logic
│   │   ├── components/        # React components
│   │   ├── context/           # React context providers
│   │   ├── hooks/             # Custom React hooks
│   │   ├── layouts/           # Layout components
│   │   ├── pages/             # Page components
│   │   ├── routes/            # Route configuration
│   │   ├── theme/             # Theme configuration
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx            # Main App component
│   │   └── main.jsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── tailwind.config.js     # Tailwind CSS configuration
│
└── README.md                  # This file
```

---

## API Documentation

### Swagger/OpenAPI Documentation

Once the backend is running, access the interactive API documentation:

```
http://localhost:8000/docs
```

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user

#### Documents
- `GET /api/v1/documents/` - List user's documents
- `POST /api/v1/documents/upload` - Upload a new document
- `DELETE /api/v1/documents/{id}` - Delete a document

#### Chat
- `GET /api/v1/chat/sessions` - Get chat sessions
- `POST /api/v1/chat/sessions` - Create new chat session
- `POST /api/v1/chat/message` - Send message and get RAG response
- `GET /api/v1/chat/history/{session_id}` - Get chat history

#### Admin (Requires Admin Role)
- `GET /api/v1/admin/users` - List all users
- `PUT /api/v1/admin/users/{id}` - Update user
- `DELETE /api/v1/admin/users/{id}` - Delete user

---

## Database

### Database Schema

The application uses SQLite with the following main tables:

- **users** - User accounts and credentials
- **chat_sessions** - Conversation sessions
- **chat_messages** - Individual messages in sessions
- **documents** - Uploaded documents metadata
- **token_blacklist** - Invalidated JWT tokens

### Creating & Running Migrations

**For Fresh Setup (Initial Migration):**

```bash
cd backend
# Create the initial migration from your models
alembic revision --autogenerate -m "Initial schema"
# Apply the migration to create tables
alembic upgrade head
```

**For Existing Setup (After Model Changes):**

```bash
# 1. Create a new migration
alembic revision --autogenerate -m "Description of changes"
# 2. Review the generated migration file in backend/alembic/versions/
# 3. Apply the migration
alembic upgrade head
```

**To Rollback Migrations:**

```bash
# Downgrade to previous version
alembic downgrade -1
# Or downgrade to specific version
alembic downgrade <revision_id>
```

### Database Location

- SQLite database: `backend/rag_app.db`
- ChromaDB storage: `backend/chroma_db/`

---

## Authentication

### JWT Authentication

The application uses JSON Web Tokens (JWT) for authentication:

1. User logs in with credentials
2. Server returns `access_token` and `refresh_token`
3. Client sends `access_token` in `Authorization: Bearer <token>` header
4. Tokens expire and can be refreshed using `refresh_token`

### Protected Routes

All API endpoints (except `/auth/login` and `/auth/register`) require authentication. Include the JWT token in the request header:

```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/v1/documents/
```

---

## Contributing

### Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests and linting
4. Commit with meaningful messages: `git commit -m "Add: feature description"`
5. Push to branch: `git push origin feature/your-feature`
6. Create a Pull Request

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ESLint configuration provided
- **Commits**: Use conventional commit format

### Testing

Run evaluation tests:

```bash
cd backend/evaluation
python run_ragas_gemini_eval.py
python run_ragas_llama_hf_eval.py
python run_free_eval.py
```

---

## Troubleshooting

### Common Issues

**Issue**: "Module not found" errors
- **Solution**: Ensure virtual environment is activated: `source venv/bin/activate`

**Issue**: Port already in use (8000 or 5173)
- **Solution**: Change port in command: `--port 8001` for backend or `--port 5174` for frontend

**Issue**: ChromaDB errors
- **Solution**: Delete `chroma_db/` directory and restart: `rm -rf backend/chroma_db/`

**Issue**: Database locked error
- **Solution**: Close all connections and delete `.db` file: `rm backend/rag_app.db`

**Issue**: "No such revision" error when running `alembic upgrade head`
- **Solution**: You need to create the initial migration first:
  ```bash
  cd backend
  alembic revision --autogenerate -m "Initial schema"
  alembic upgrade head
  ```

**Issue**: "Can't locate revision identified by" error
- **Solution**: Make sure migration files exist in `backend/alembic/versions/`:
  ```bash
  ls backend/alembic/versions/
  # Should show files like: 45317c81b019_initial_schema.py
  ```
  If no files exist, create them: `alembic revision --autogenerate -m "Initial schema"`

---

## Future Enhancements

- [ ] Implement PostgreSQL for production scalability
- [ ] Add Redis caching layer
- [ ] Implement rate limiting and API quotas
- [ ] Add two-factor authentication (2FA)
- [ ] Support for more document formats (PPT, Web links)
- [ ] Real-time collaborative chat
- [ ] Advanced analytics and usage tracking
- [ ] Multi-language support
- [ ] Horizontal scaling with Docker/Kubernetes

---

## License

This project is provided as-is for educational and research purposes.

---

## Support & Contact

For issues, questions, or suggestions:
1. Check the documentation above
2. Review the API documentation at `/docs`
3. Check troubleshooting section
4. Open an issue in the repository

---

## Version History

- **v1.0.0** (Current) - Initial release with core RAG functionality

---

**Last Updated**: May 13, 2026

