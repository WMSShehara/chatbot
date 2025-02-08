import google.generativeai as genai
from config import Gemini_API_KEY  # Ensure this file contains your API key

# Configure the API
genai.configure(api_key=Gemini_API_KEY)

def generate_answer(context: str, query: str) -> str:
    """
    Generate an answer using Google's Gemini API
    
    Args:
        query (str): The user's question
        
    Returns:
        str: The generated answer or an error message
    """
    try:
        # Load the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Construct the prompt
        prompt = f"context: {context}\n\nQuestion: {query}\n\nAnswer:"
        
        # Generate content
        # optimization: max_output_tokens: 200
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 200})

        

        # Extract text from the response
        if response and hasattr(response, "text"):
            return response.text.strip()
        return "Sorry, I couldn't generate an answer."
    
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"


