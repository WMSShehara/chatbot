import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_answer(context: str, query: str) -> str:
    """
    Generate an answer to the query based on the retrieved context using GPT-3 or GPT-4.
    
    Args:
        context: The retrieved text chunks as context for the answer.
        query: The user's query.
    
    Returns:
        A string containing the generated answer.
    """
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    
    # Call OpenAI API to generate an answer using the new Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or use "gpt-4" for a newer model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # Limit the response length
        temperature=0.7,  # Control the creativity of the response
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    return answer

def main():
    """
    Example to run the query, retrieve similar chunks, and generate an answer.
    """
    from store_embeddings import load_embeddings
    from retrieve_embeddings import retrieve_similar_chunks
    from embed_text import load_model
    import numpy as np

    # Path to your saved FAISS index and chunks file
    index_file = "embeddings_store.faiss"
    chunks_file = "embeddings_store_chunks.npy"

    # Load the model and embeddings
    model = load_model()
    index, loaded_chunks = load_embeddings(index_file, chunks_file)

    # Input query from the user
    query = input("Enter your query: ")

    # Retrieve similar chunks from FAISS
    similar_chunks, distances = retrieve_similar_chunks(query, index, loaded_chunks, model)

    # Combine the top relevant chunks into a single context (you can adjust how many chunks you want to use)
    context = " ".join(similar_chunks[:3])  # Taking the top 3 chunks

    # Generate an answer using GPT
    answer = generate_answer(context, query)

    # Print the generated answer
    print(f"Generated Answer: {answer}")

if __name__ == "__main__":
    main()
