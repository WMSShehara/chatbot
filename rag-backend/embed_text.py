from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

def load_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Load the pre-trained SentenceTransformer model.
    """
    return SentenceTransformer(model_name)

def generate_embeddings(chunks: List[str], model: SentenceTransformer) -> np.ndarray:
    """
    Generate embeddings for a list of text chunks.
    
    Args:
        chunks: A list of text strings to embed.
        model: The loaded SentenceTransformer model.
    
    Returns:
        A NumPy array containing the embeddings.
    """
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings

# test the functions
if __name__ == "__main__":
    # Example usage
    from process_data import extract_text_pymupdf, clean_text, split_into_chunks
    
    # Path to your PDF
    pdf_path = "BioResoBook.pdf"
    
    # Preprocess the text
    raw_text = extract_text_pymupdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    chunks = split_into_chunks(cleaned_text)
    
    # Load the model and generate embeddings
    model = load_model()
    embeddings = generate_embeddings(chunks, model)
    
    # Display results
    print(f"Generated {len(embeddings)} embeddings with shape {embeddings.shape}.")
