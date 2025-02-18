from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os


import torch
import torch.nn as nn
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
n_gpu = torch.cuda.device_count()
from transformers import BertTokenizer,BertModel

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from pytorch_pretrained_bert import BertTokenizer, BertConfig
from pytorch_pretrained_bert import BertAdam, BertForSequenceClassification
from tqdm import tqdm, trange
import pandas as pd
import io
import numpy as np


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

@app.post("/ask", response_model=QueryResponse)
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


@app.post("/llm", response_model=QueryResponse)
def ask_model_question(request: QueryRequest):
    # Load English BERT tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model1 = BertModel.from_pretrained('bert-base-uncased')

    paragraphs=[]
    questions=[]
    answers=[]
    f = open("data/paragraphs.json", "r+")
    q = open("data/questions.json", "r+")
    a = open("data/answers.json", "r+")

    for x in f:
        paragraphs.append(x)
    for x in q:
        questions.append(x)
    for x in a:
        answers.append(x)
    print(len(paragraphs),len(questions),len(answers))


    return len(paragraphs),len(questions),len(answers), answers[1]