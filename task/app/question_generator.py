
"""
Core logic to generate technical questions using Google Gemini API.
"""
import os
import requests
from dotenv import load_dotenv
from prompts import question_prompt

# Load environment variables
load_dotenv()

def generate_questions(tech_stack: list) -> list:
    """
    Generate 3-5 technical questions per technology using Google Gemini API.
    Args:
        tech_stack (list): List of technologies.
    Returns:
        list: List of generated questions.
    """
    prompt = question_prompt(tech_stack)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}
    try:
        resp = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        questions = []
        for line in content.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                q = line.lstrip("0123456789.- ")
                if q:
                    questions.append(q)
        if not questions:
            questions = [content]
        return questions[:5]
    except Exception as e:
        # Fallback to sample questions when API is unavailable
        if "503" in str(e) or "429" in str(e) or "overloaded" in str(e) or "quota" in str(e):
            return get_fallback_questions(tech_stack)
        return [f"Error generating questions: {e}"]

def get_fallback_questions(tech_stack: list) -> list:
    """Provide fallback questions when API is unavailable."""
    fallback_questions = {
        "Python": [
            "Explain the difference between lists and tuples in Python.",
            "How do you handle exceptions in Python? Provide an example.",
            "What are decorators in Python? Give a practical example.",
            "Explain the concept of generators in Python.",
            "How does Python's garbage collection work?"
        ],
        "Django": [
            "What is Django ORM and how does it work?",
            "Explain Django's MVT (Model-View-Template) architecture.",
            "How do you handle database migrations in Django?",
            "What are Django signals and when would you use them?",
            "Explain Django's authentication system."
        ],
        "JavaScript": [
            "Explain the difference between var, let, and const.",
            "What are closures in JavaScript? Provide an example.",
            "Explain the concept of promises and async/await.",
            "How does JavaScript handle hoisting?",
            "What is the event loop in JavaScript?"
        ],
        "React": [
            "Explain the difference between state and props in React.",
            "What are React hooks? Give examples of useState and useEffect.",
            "Explain the concept of virtual DOM in React.",
            "How do you handle component lifecycle in React?",
            "What is the difference between controlled and uncontrolled components?"
        ],
        "Node.js": [
            "Explain the event-driven nature of Node.js.",
            "What is the difference between require and import?",
            "How do you handle asynchronous operations in Node.js?",
            "Explain the concept of streams in Node.js.",
            "What are middleware functions in Express.js?"
        ]
    }
    
    questions = []
    for tech in tech_stack:
        tech_lower = tech.lower()
        for key, tech_questions in fallback_questions.items():
            if key.lower() in tech_lower or tech_lower in key.lower():
                questions.extend(tech_questions)
                break
        else:
            # Generic questions for unknown technologies
            questions.extend([
                f"Explain the core concepts of {tech}.",
                f"What are the best practices for {tech}?",
                f"How would you troubleshoot common issues in {tech}?",
                f"What are the key features of {tech}?",
                f"How would you optimize performance in {tech}?"
            ])
    
    return questions[:5]  # Return max 5 questions
