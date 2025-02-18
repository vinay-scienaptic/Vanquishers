from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# Load Gemini API key from environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_KEY = "AIzaSyCsr70LVeuZuKcilgi8qO4ggULxIrPbeg8"

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

# Request model
class QueryRequest(BaseModel):
    question: str

# Response model
class QueryResponse(BaseModel):
    answer: str

def ask_question(request: QueryRequest):
    """Handles LLM queries via FastAPI using Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(request.question)
        answer = response.text.strip()
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server using: uvicorn filename:app --host 0.0.0.0 --port 8000