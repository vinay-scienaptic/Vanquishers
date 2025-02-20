from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware
import textwrap
 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

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
        rules = " If any request like writing code ,giving weather update comes, Then just mention -> Sorry for the inconvinicen cause. Please ask question related to Scienaptic organization. Also treat Scienaptic as ours not theres.IF any random letter or number or character is given return Sorry for the inconviniece"
        prompt = f"{scienaptic_data} Please provide a concise answer to the following question in 5 lines or less: {request.question}"
        response = model.generate_content(prompt)
        answer = response.text.strip()
 
        # Limit the response to 5 lines
        limited_answer = limit_answer_to_lines(answer, max_lines=5)
 
        return QueryResponse(answer=limited_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
# Run the server using: uvicorn filename:app --host 0.0.0.0 --port 8000

@app.post("/schedule", response_model=QueryResponse)
def schedule_call(request: QueryResponse):
    # Authenticate with OAuth 2.0
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    CLIENT_ID = os.getenv("CALENDER_CLIENT_ID")
    PROJECT_ID = os.getenv("CALENDER_PROJECT_ID")
    CLIENT_SECRET = os.getenv("CALENDAR_CLIENT_SECRET")

    SERVICE_ACCOUNT_FILE = "creds.json"
    
    creds_dict = {"web":{"client_id":CLIENT_ID,"project_id":PROJECT_ID,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":CLIENT_SECRET}}

    #"urn:ietf:wg:oauth:2.0:oob" 
    # Load OAuth 2.0 credentials and start authentication flow
    flow = InstalledAppFlow.from_client_config(creds_dict,scopes=["https://www.googleapis.com/auth/drive"],redirect_uri="https://vanquishers.scienaptic.com/" )
    credentials = flow.run_local_server(port=0) 


    # Convert to Credentials object
    # credentials = Credentials.from_authorized_user_info(creds_data)


    service = build('calendar', 'v3', credentials=credentials)


    # Step 2: Define event details
    event = {
        'summary': 'Project Call',
        'location': 'Google Meet',
        'description': 'Discuss project updates',
        'start': {
            'dateTime': '2025-02-20T10:00:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2025-02-20T11:00:00',
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': 'vinay.pottabathini@scienaptic.com'},
            {'email': 'vinay040998@gmail.com'},
            
        ],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': 'meet12345'
            }
        }
    }

    # Step 3: Create event and send invites
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,  # Required for Google Meet link
        sendUpdates='all'  # Sends email invites
    ).execute()

    print(f"Event created: {event.get('htmlLink')}")
    return None
