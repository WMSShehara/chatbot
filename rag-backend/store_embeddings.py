import faiss
import numpy as np
from typing import List

def store_embeddings(embeddings: np.ndarray, chunks: List[str], output_file: str) -> None:
    """
    Store embeddings and their associated chunks in a FAISS index.
    
    Args:
        embeddings: The NumPy array of embeddings.
        chunks: The list of text chunks corresponding to the embeddings.
        output_file: The path to save the FAISS index and chunk mappings.
    """
    # Create a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the FAISS index
    faiss.write_index(index, f"{output_file}.faiss")

    # Save the chunks as a NumPy object
    np.save(f"{output_file}_chunks.npy", chunks)
    print(f"Embeddings and chunks saved to {output_file}.faiss and {output_file}_chunks.npy")

def load_embeddings(index_file: str, chunks_file: str):
    """
    Load a FAISS index and associated chunks.
    
    Args:
        index_file: Path to the FAISS index file.
        chunks_file: Path to the chunks file.
    
    Returns:
        A tuple of the FAISS index and the list of chunks.
    """
    index = faiss.read_index(index_file)
    chunks = np.load(chunks_file, allow_pickle=True)
    return index, chunks

# test the functions
if __name__ == "__main__":
    # Example usage
    from embed_text import generate_embeddings, load_model
    from process_data import extract_text_pymupdf, clean_text, split_into_chunks

    # Path to PDF
    pdf_path = "BioResoBook.pdf"

    # Preprocess text
    raw_text = extract_text_pymupdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    chunks = split_into_chunks(cleaned_text)

    # Generate embeddings
    model = load_model()
    embeddings = generate_embeddings(chunks, model)

    # Store embeddings
    output_file = "embeddings_store"
    store_embeddings(embeddings, chunks, output_file)

    # Load embeddings
    index, loaded_chunks = load_embeddings(f"{output_file}.faiss", f"{output_file}_chunks.npy")
    print(f"Loaded {len(loaded_chunks)} chunks from {output_file}.")
