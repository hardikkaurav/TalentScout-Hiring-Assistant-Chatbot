"""
Answer evaluation module for TalentScout Hiring Assistant.
Evaluates candidate answers using Google Gemini API.
"""
import os
import requests
from dotenv import load_dotenv
from prompts import evaluation_prompt

# Load environment variables
load_dotenv()

def evaluate_answer(question: str, answer: str) -> dict:
    """
    Evaluate a candidate's answer to a technical question.
    Args:
        question (str): The technical question asked.
        answer (str): The candidate's answer.
    Returns:
        dict: Evaluation result with score (0-10) and feedback.
    """
    prompt = evaluation_prompt(question, answer)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        return get_fallback_evaluation(question, answer)
    
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
        
        # Parse the evaluation response
        evaluation = parse_evaluation_response(content)
        return evaluation
        
    except Exception as e:
        # Fallback to sample evaluation when API is unavailable
        if "503" in str(e) or "429" in str(e) or "overloaded" in str(e) or "quota" in str(e):
            return get_fallback_evaluation(question, answer)
        return {
            "score": 5,
            "feedback": f"Error evaluating answer: {e}. Please try again."
        }

def parse_evaluation_response(content: str) -> dict:
    """Parse the evaluation response from Gemini API."""
    try:
        # Look for score pattern (e.g., "Score: 8/10" or "8/10")
        import re
        score_match = re.search(r'(\d+)/10', content)
        score = int(score_match.group(1)) if score_match else 5
        
        # Extract feedback (everything after the score)
        feedback = content
        if score_match:
            feedback = content[score_match.end():].strip()
        
        # Clean up feedback
        feedback = feedback.replace("Feedback:", "").strip()
        if not feedback:
            feedback = "Good attempt! Keep practicing."
        
        return {
            "score": min(max(score, 0), 10),  # Ensure score is between 0-10
            "feedback": feedback
        }
    except Exception:
        return {
            "score": 5,
            "feedback": "Good attempt! Keep practicing."
        }

def get_fallback_evaluation(question: str, answer: str) -> dict:
    """Provide fallback evaluation when API is unavailable."""
    # Simple keyword-based evaluation
    answer_lower = answer.lower()
    question_lower = question.lower()
    
    score = 5  # Default score
    
    # Check for technical keywords based on question type
    if "python" in question_lower:
        python_keywords = ["def", "class", "import", "try", "except", "list", "tuple", "dict", "decorator", "generator"]
        score += sum(2 for keyword in python_keywords if keyword in answer_lower)
    elif "javascript" in question_lower or "js" in question_lower:
        js_keywords = ["function", "const", "let", "var", "async", "await", "promise", "closure", "hoisting"]
        score += sum(2 for keyword in js_keywords if keyword in answer_lower)
    elif "react" in question_lower:
        react_keywords = ["component", "state", "props", "hook", "useState", "useEffect", "virtual", "dom"]
        score += sum(2 for keyword in react_keywords if keyword in answer_lower)
    elif "django" in question_lower:
        django_keywords = ["model", "view", "template", "orm", "migration", "signal", "authentication"]
        score += sum(2 for keyword in django_keywords if keyword in answer_lower)
    
    # Check answer length and quality
    if len(answer) > 100:
        score += 1
    if len(answer) > 200:
        score += 1
    
    # Check for code examples
    if "```" in answer or "def " in answer or "function " in answer:
        score += 2
    
    # Ensure score is between 0-10
    score = min(max(score, 0), 10)
    
    # Generate feedback based on score
    if score >= 8:
        feedback = "Excellent answer! You demonstrate strong technical knowledge."
    elif score >= 6:
        feedback = "Good answer! You show solid understanding of the concept."
    elif score >= 4:
        feedback = "Fair attempt. Consider providing more specific examples and technical details."
    else:
        feedback = "Try to provide more detailed technical explanations with examples."
    
    return {
        "score": score,
        "feedback": feedback
    } 