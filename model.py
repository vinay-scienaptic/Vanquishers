from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware
import textwrap
 
# Initialize FastAPI app
app = FastAPI()
 
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify specific ones
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
 
# Load Gemini API key from environment variables
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = "AIzaSyCsr70LVeuZuKcilgi8qO4ggULxIrPbeg8"
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Set the GEMINI_API_KEY environment variable.")
genai.configure(api_key=GEMINI_API_KEY)
 
# Request model for incoming query
class QueryRequest(BaseModel):
    question: str
 
# Response model for API response
class QueryResponse(BaseModel):
    answer: str
 
def limit_answer_to_lines(text, max_lines=5):
    """
    Limits the answer to a maximum number of lines.
    This splits the text by new lines and truncates it to the required number of lines.
    """
    # Split the answer by newlines and only take the first 'max_lines' lines
    lines = text.split("\n")
    limited_lines = lines[:max_lines]  # Take only the first 'max_lines' lines
    return "\n".join(limited_lines)
 
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """Handles LLM queries via FastAPI using Gemini."""
    try:
        # Use the generative model to get the response
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Prompt modification: Ask the model for a summary or concise answer
        scienaptic_data= "We are Scienaptic!!! Founded in 2014, Scienaptic AI was built with a mission to drive financial inclusion at scale through AI-driven credit decisioning. Our platform encapsulates over 200 years of combined credit risk expertise and a decade of technological innovation, integrating diverse data sources, advanced machine learning algorithms, and comprehensive risk and fair lending monitoring processes. Our Mission: Increase credit availability. We are a CUSO driven by a coalition of visionary credit unions. Leadership Team Investors & Advisers Our Mission: Increase credit availability. Credit administration is handicapped by old credit underwriting technology. We are on a mission to change that. We are a CUSO driven by a coalition of visionary credit unions. Out credit union clients: Credit Union of Colorado Covantage Credit Union People Driven Credit Union Wildfire Credit Union Elga Credit Union 4front Credit Union Alliance Catholic Credit Union Partner Colorado Credit Union Advantage One Credit Union Michigan Credit Union League Leadership Team Pankaj Kulshrestha (CEO) Eric Steinhoff (Client Impact) Vinay Bhaskar (AI / Risk Innovation) Joydip Gupta (Business Leader - APAC) Samantha Hubbard (Business Development) Gregory Bishop (Business Development) Abhishek Sharma (Engineering) Chandan Pal (Marketing) Investors & Advisers Pramod Bhasin Ray Duggins Francisco D'Souza Michael Heller Kevin Oden."
        prompt = f"{scienaptic_data} Please provide a concise answer to the following question in 5 lines or less: {request.question}"
        response = model.generate_content(prompt)
        answer = response.text.strip()
 
        # Limit the response to 5 lines
        limited_answer = limit_answer_to_lines(answer, max_lines=5)
 
        return QueryResponse(answer=limited_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
# Run the server using: uvicorn filename:app --host 0.0.0.0 --port 8000