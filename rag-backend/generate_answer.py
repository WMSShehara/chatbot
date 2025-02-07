import google.generativeai as genai
from config import Gemini_API_KEY

genai.configure(api_key=Gemini_API_KEY)

def generate_answer(context: str, query: str) -> str:
    """
    Generate an answer using Google's Gemini API
    """
    # Structure the prompt as a conversation
    prompt = {
        "contents": [{
            "parts":[{
                "text": f"Context: {context}\n\nQuestion: {query}\nAnswer:"
            }]
        }]
    }
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    if response.text:
        return response.text
    return "Sorry, I couldn't generate an answer."

