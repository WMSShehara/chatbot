# ASKPDF - Retrieval-Augmented Generation Application (RAG)

This individual project implements a Retrieval-Augmented Generation (RAG) application for answering user queries based on uploaded documents. The application consists of a FastAPI backend and a React frontend, enabling users to upload documents, generate embeddings, and retrieve answers to their queries.

## Table of content

- [Installation and Run Locally](#installation-and-run-locally)
- [Components](#components)
- [API Reference](#API-reference)

## Installation-and-run-locally

### Backend

1. clone the repository
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
4. Create config.py and include OPENAI_API_KEY : 
```bash
    OPENAI_API_KEY="your OPENAI_API_KEY"
```
5.   Run the Backend: 
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

- process_data.py : extract text from file, remove the unnecessary special characters and white spaces and split into chunks.
- embed_text.py : generate embeddings for a list of text chunks and load the pre trained sentence tranformer model
- store_embeddings.py : store embeddings and their associated chunks in FAISS index and load the FAISS index and associated chunks.
- retrieve_embedings.py : retrieve the top and most similar chuns for a given query.
- generate_answer.py : generate answer based on the retrieved context using GPT

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



