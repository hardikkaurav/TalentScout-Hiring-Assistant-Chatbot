"""
Optional FastAPI backend for TalentScout Hiring Assistant Chatbot.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from question_generator import generate_questions
from utils import save_candidate_info
from dotenv import load_dotenv
from typing import List, Any, Dict

# Load environment variables
load_dotenv()

app = FastAPI()

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    experience: int
    position: str
    location: str
    tech_stack: List[str]
    questions: List[str] = []

@app.post("/generate_questions")
def api_generate_questions(payload: Dict[str, Any]):
    tech_stack = payload.get("tech_stack", [])
    if not tech_stack:
        raise HTTPException(status_code=400, detail="Tech stack required.")
    questions = generate_questions(tech_stack)
    return {"questions": questions}

@app.post("/save_candidate")
def api_save_candidate(candidate: Candidate):
    save_candidate_info(candidate.dict())
    return {"status": "success"}
