from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from process_data import extract_text_from_pdf, clean_text, split_into_chunks
from embed_text import load_model, generate_embeddings
from store_embeddings import store_embeddings, load_embeddings
from retrieve_embeddings import retrieve_similar_chunks
from generate_answer import generate_answer
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model once at startup to avoid reloading it for each request
model = load_model()

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file for processing.
    """
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract and process the file's text
        raw_text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(raw_text)
        chunks = split_into_chunks(cleaned_text)

        # Generate and store embeddings
        embeddings_file_base = os.path.join(UPLOAD_DIR, os.path.splitext(file.filename)[0] + "_embeddings")
        embeddings = generate_embeddings(chunks, model)
        store_embeddings(embeddings, chunks, embeddings_file_base)

        return {"message": "File processed and embeddings stored successfully.", "file_name": file.filename, "file_path": file_path}

    except Exception as e:
        return JSONResponse(content={"error": f"Failed to process the file: {str(e)}"}, status_code=500)

@app.post("/ask-question/")
async def ask_question(
    query: str = Form(...), 
    file_name: str = Form(...)
):
    """
    Endpoint to retrieve answers based on a query and previously uploaded file.
    """
    try:
        # Construct the file paths for embeddings
        embeddings_file_base = os.path.join(UPLOAD_DIR, os.path.splitext(file_name)[0] + "_embeddings")
        index_file = f"{embeddings_file_base}.faiss"
        chunks_file = f"{embeddings_file_base}_chunks.npy"

        # Check if embeddings exist for the specified file
        if not os.path.exists(index_file) or not os.path.exists(chunks_file):
            return JSONResponse(content={"error": "Embeddings for the specified file do not exist."}, status_code=404)

        # Load embeddings
        index, loaded_chunks = load_embeddings(index_file, chunks_file)

        # Retrieve similar chunks
        similar_chunks, distances = retrieve_similar_chunks(query, index, loaded_chunks, model)

        # Combine relevant chunks into context
        context = " ".join(similar_chunks[:3])  # Adjust number of chunks as needed

        # Generate an answer using the context
        answer = generate_answer(context, query)

        return {"query": query, "answer": answer}

    except Exception as e:
        return JSONResponse(content={"error": f"Failed to process the query: {str(e)}"}, status_code=500)
