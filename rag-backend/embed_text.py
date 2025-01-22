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

