# uvicorn main:app --reload
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from process_data import (
    extract_text_from_pdf,
    clean_text_content,
    split_into_chunks,
    process_pdf,
    generate_enhanced_context
)
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

# Add to global state
kg_builders = {}

# test the api
#http://127.0.0.1:8000/docs

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file for processing.
    """
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        try:
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            print(f"File saved successfully to {file_path}")
        except Exception as save_error:
            print(f"Error saving file: {str(save_error)}")
            raise save_error

        try:
            # Process file and build knowledge graph
            print("Starting PDF processing...")
            text, kg_builder = process_pdf(file_path)
            print("PDF processed successfully")
            
            kg_builders[file.filename] = (text, kg_builder)
            print("Knowledge graph built successfully")

            return {"message": "File processed successfully", "file_name": file.filename}

        except Exception as process_error:
            print(f"Error processing PDF: {str(process_error)}")
            raise process_error

    except Exception as e:
        print(f"Upload error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return JSONResponse(
            content={
                "error": f"Failed to process file: {str(e)}",
                "error_type": str(type(e).__name__)
            }, 
            status_code=500
        )

@app.post("/ask-question/")
async def ask_question(query: str = Form(...), file_name: str = Form(...)):
    """
    Endpoint to retrieve answers based on a query and previously uploaded file.
    """
    try:
        if file_name not in kg_builders:
            return JSONResponse(content={"error": "File not found"}, status_code=404)
        
        try:
            text, kg_builder = kg_builders[file_name]
            enhanced_context = generate_enhanced_context(query, text, kg_builder)
            answer = generate_answer(enhanced_context, query)
            
            # Get graph visualization data
            graph_data = kg_builder.get_graph_data(query)
            
            return {
                "answer": answer,
                "graph_data": graph_data
            }
        except Exception as inner_e:
            print(f"Processing error: {str(inner_e)}")  # Add logging
            raise inner_e

    except Exception as e:
        print(f"Error in ask_question: {str(e)}")  # Add logging
        return JSONResponse(
            content={
                "error": f"Failed to process query: {str(e)}",
                "details": str(e.__class__.__name__)
            }, 
            status_code=500
        )
