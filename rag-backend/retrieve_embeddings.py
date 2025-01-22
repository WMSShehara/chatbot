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

if __name__ == "__main__":
    # Example usage
    from embed_text import load_model
    from store_embeddings import load_embeddings

    # Path to your saved FAISS index and chunks file
    index_file = "embeddings_store.faiss"
    chunks_file = "embeddings_store_chunks.npy"

    # Load model
    model = load_model()

    # Load the FAISS index and chunks
    index, loaded_chunks = load_embeddings(index_file, chunks_file)

    # Query input from the user
    query = input("Enter your query: ")

    # Retrieve similar chunks
    similar_chunks, distances = retrieve_similar_chunks(query, index, loaded_chunks, model)

    # Display the results
    print("Top similar chunks:")
    for i, (chunk, dist) in enumerate(zip(similar_chunks, distances)):
        print(f"Rank {i + 1}:")
        print(f"Chunk: {chunk}")
        print(f"Distance: {dist}")