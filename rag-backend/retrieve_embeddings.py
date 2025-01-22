import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

def retrieve_similar_chunks(query: str, index: faiss.Index, chunks: List[str], model: SentenceTransformer, top_k: int = 5):
    """
    Retrieve the top_k most similar chunks for a given query.
    
    Args:
        query: The query string to search for.
        index: The FAISS index containing embeddings.
        chunks: The list of text chunks.
        model: The pre-trained SentenceTransformer model for embedding the query.
        top_k: The number of top similar chunks to return.
    
    Returns:
        A list of the top_k most similar chunks.
    """
    # Encode the query into an embedding
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search the index for the nearest neighbors
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve the top_k similar chunks
    similar_chunks = [chunks[i] for i in indices[0]]
    return similar_chunks, distances[0]

