"""
Prompt templates for TalentScout Hiring Assistant Chatbot.
"""

def info_prompt(field_label: str) -> str:
    """Prompt for collecting candidate details."""
    return f"Please provide your {field_label}."

def question_prompt(tech_stack: list) -> str:
    """Chain-of-thought prompt for generating technical questions."""
    techs = ', '.join(tech_stack)
    return (
        f"You are a technical interviewer. Given the following tech stack: {techs}, "
        "generate 3-5 specific technical interview questions. "
        "Questions should be clear, relevant, and test practical knowledge. "
        "Format each question as a numbered list starting with 1. "
        "Focus on actual technical questions, not domain categories."
    )

def evaluation_prompt(question: str, answer: str) -> str:
    """Prompt for evaluating candidate answers."""
    return (
        f"You are a technical interviewer evaluating a candidate's answer. "
        f"Question: {question}\n"
        f"Candidate's Answer: {answer}\n\n"
        f"Please evaluate this answer on a scale of 0-10 and provide constructive feedback. "
        f"Consider:\n"
        f"- Technical accuracy and depth\n"
        f"- Practical examples provided\n"
        f"- Code quality (if applicable)\n"
        f"- Clarity of explanation\n\n"
        f"Respond in this format:\n"
        f"Score: X/10\n"
        f"Feedback: [Your detailed feedback here]"
    )

def fallback_prompt(field_label: str) -> str:
    """Prompt for handling off-topic or misunderstood input."""
    return (
        f"Sorry, I didn't understand your response for {field_label}. "
        "Could you please rephrase or provide a valid input?"
    )
