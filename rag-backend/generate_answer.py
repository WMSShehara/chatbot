import google.generativeai as genai
from config import Gemini_API_KEY

# Configure the API key for Google's generative AI
genai.configure(api_key=Gemini_API_KEY)

def generate_answer(context: str, query: str) -> str:
    """
    Generate an answer using Google's Gemini API.
    
    Args:
        context (str): The context information to base the answer on.
        query (str): The user's question.
        
    Returns:
        str: The generated answer or an error message.
    """
    try:
        # Create the prompt as a single string
        prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
        
        # Call the API using the generate_text method
        response = genai.generate_text(
            model="models/gemini-1.5-flash",  # Use your target model; update if needed.
            prompt=prompt,
            temperature=0.2,
            max_output_tokens=512
        )
        
        # Check if the response contains candidates and return the first candidate's text
        if response and response.candidates:
            return response.candidates[0].text.strip()
        return "Sorry, I couldn't generate an answer."
        
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"
