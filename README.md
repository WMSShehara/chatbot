# ASKPDF - Retrieval-Augmented Generation Application (RAG)

This individual project implements a Retrieval-Augmented Generation (RAG) application for answering user queries based on uploaded documents. The application consists of a FastAPI backend and a React frontend, enabling users to upload documents, generate embeddings, and retrieve answers to their queries.

## Table of content

- [Tech Stack](#tech-stack)
- [Installation and Run Locally](#installation-and-run-locally)
- [Components](#components)
- [API Reference](#API-reference)

## Tech Stack

### Frontend
- **Framework**: React.js
- **UI Components**: Material-UI (MUI)
- **HTTP Client**: Axios
- **State Management**: React Hooks
- **Styling**: CSS Modules

### Backend
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **API Documentation**: Swagger/OpenAPI

### RAG Pipeline
- **LLM Integration**: Google Gemini Pro
- **Embeddings**: Sentence-Transformers
- **Vector Storage**: FAISS
- **Document Processing**: 
  - PyPDF (PDF processing)
  - Pandas (Data handling)
  - NumPy (Numerical operations)

### Development Tools
- **Environment Management**: 
  - Python: venv
  - Node.js: npm
- **API Validation**: Pydantic
- **Version Control**: Git
- **Code Formatting**: 
  - Python: Black
  - JavaScript: Prettier

## Installation-and-run-locally

### Backend

1. Clone the repository
```bash
    git clone <repository_url>
    cd rag-backend
```
2. Set Up a Virtual Environment:
```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```
3. Install dependencies
```bash
    pip install -r requirements.txt
``` 
4. Create config.py and include Gemini API key: 
```bash
    Gemini_API_KEY="your-gemini-api-key-here"
```
5. Run the Backend: 
```bash
    uvicorn main:app --reload
```

### Frontend

1. Navigate to Frontend
```bash
    cd rag-frontend
```
2. Install dependencies
```bash
    npm install
```
3. Start the frontend:
```bash
    npm start
```
## Components

### Frontend components

- FileUpload.js : handle the file uploading
- Page.js : handle the user queries

### Backend components

- **process_data.py**: Document Processing Pipeline
  - PyPDF: Extract text from PDF files
  - Regular Expressions (re): Clean and sanitize text
  - LangChain Text Splitter: Split documents into manageable chunks
  - NumPy: Handle text arrays and numerical operations

- **embed_text.py**: Embedding Generation
  - Sentence-Transformers: Generate text embeddings
  - Model: 'all-MiniLM-L6-v2' for efficient text embedding
  - NumPy: Handle embedding vectors
  - Torch: Backend for transformer models

- **store_embeddings.py**: Vector Storage
  - FAISS: High-performance similarity search
  - NumPy: Vector operations and data handling
  - Pickle: Serialize and store index data
  - OS: File handling and path management

- **retrieve_embeddings.py**: Similarity Search
  - FAISS: Vector similarity search
  - NumPy: Vector operations
  - Sentence-Transformers: Query embedding generation
  - Heapq: Manage top-k similar chunks

- **generate_answer.py**: Answer Generation
  - Google Gemini Pro: Generate contextual answers
  - google.generativeai: Gemini API integration
  - Prompt Templates: Structure system and user prompts
  - JSON: Handle API responses

- **main.py**: API Endpoints
  - FastAPI: Web framework
  - Pydantic: Request/response validation
  - Uvicorn: ASGI server
  - Python-multipart: Handle file uploads

## API-reference

### File upload

#### Endpoint: 
```http
  /upload-file/
```
#### Method:
```http
  POST
```
#### Description : 
```http
  Accepts a file for processing.
```
#### Response:
```http
  {
  "message": "File processed and embeddings stored successfully.",
  "file_name": "uploaded_file_name",
  "file_path": "path_to_uploaded_file"
}
```

#### Ask a question

#### Endpoint: 
```http
  /ask-question/
```
#### Method:
```http
  POST
```
#### Description : 
```http
  Ask question based on file.
```
#### Parameters : 
```http
    query: User's question.
    file_name: Name of the file for which embeddings were generated
```
#### Response:
```http
{
  "query": "Your question",
  "answer": "Generated answer based on the document"
}
```



