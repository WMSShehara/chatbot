from fastapi import FastAPI
from pydantic import BaseModel
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React app to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# To simulate a model training process and a status check
model_trained = False
generated_text = ""

# Pydantic model for input data
class GenerateRequest(BaseModel):
    input_text: str

# Train model endpoint
@app.post("/train")
async def train_model():
    global model_trained
    # Simulate training with a delay
    time.sleep(2)  # Simulate training time
    model_trained = True
    return {"message": "Training completed successfully."}

# Check status endpoint
@app.get("/status")
async def check_status():
    return {"status": "Model trained" if model_trained else "Model not trained"}

# Generate text endpoint
@app.post("/generate")
async def generate_text(request: GenerateRequest):
    if not model_trained:
        return {"response": "Model not trained yet."}
    # Simulate text generation based on input
    return {"response": f"Generated text for '{request.input_text}'"}
