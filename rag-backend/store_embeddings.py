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

