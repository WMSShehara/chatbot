import google.generativeai as genai
from config import Gemini_API_KEY  # Ensure this file contains your API key

# Configure the API
genai.configure(api_key=Gemini_API_KEY)

def generate_answer(context: str, query: str) -> str:
    """
    Generate an answer using Google's Gemini API with improved context handling.
    
    Args:
        query (str): The user's question
        
    Returns:
        str: The generated answer or an error message
    """
    try:
        # Create a more structured and detailed prompt
        prompt = f"""
Based on the following context and knowledge graph information, please provide a detailed and accurate answer.
If the information is not available in the context, please say so.

CONTEXT:
{context}

QUESTION:
{query}

Please provide a comprehensive answer that:
1. Directly addresses the question
2. Uses specific information from the context
3. Maintains factual accuracy
4. Includes relevant relationships from the knowledge graph when available

ANSWER:
"""
        
        # Configure the model for more detailed output
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.3,  # Lower temperature for more focused answers
                'max_output_tokens': 800,  # Increased token limit
                'top_p': 0.8,
                'top_k': 40
            }
        )
        
        if response and hasattr(response, "text"):
            return response.text.strip()
        return "Sorry, I couldn't generate an answer based on the available information."
        
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"


