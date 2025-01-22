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

