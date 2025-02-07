import requests
import json
from config import Gemini_API_KEY


API_KEY = Gemini_API_KEY
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {"contents": [{"parts": [{"text": "Explain how AI works"}]}]}

response = requests.post(url, headers=headers, json=data)
print(response.json())