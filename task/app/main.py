"""
Streamlit app for TalentScout Hiring Assistant Chatbot.
Interactive interview system that collects candidate info and conducts technical interviews.
"""
import streamlit as st
from streamlit_chat import message
from prompts import info_prompt, fallback_prompt, evaluation_prompt
from question_generator import generate_questions
from answer_evaluator import evaluate_answer
from utils import (
    validate_email, validate_phone, save_candidate_info, sanitize_input, handle_fallback
)
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon=":briefcase:")

# Session state for conversation
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'candidate' not in st.session_state:
    st.session_state.candidate = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'interview_questions' not in st.session_state:
    st.session_state.interview_questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'interview_mode' not in st.session_state:
    st.session_state.interview_mode = False
if 'evaluation_results' not in st.session_state:
    st.session_state.evaluation_results = []

# Questions to ask for candidate info
info_questions = [
    ("name", "Full Name"),
    ("email", "Email Address"),
    ("phone", "Phone Number"),
    ("experience", "Years of Experience"),
    ("position", "Desired Position"),
    ("location", "Current Location"),
    ("tech_stack", "Tech Stack (comma-separated, e.g., Python, Django, PostgreSQL)")
]

exit_commands = ["exit", "quit", "bye"]

def is_exit(text):
    return text.strip().lower() in exit_commands


def main():
    st.title("TalentScout Hiring Assistant Chatbot")
    st.write("Welcome! I will conduct an interactive technical interview. Type 'exit' anytime to leave.")

    # ✅ Show previous chat history with unique keys
    for idx, chat in enumerate(st.session_state.chat_history):
        message(**chat, key=f"chat_{idx}")

    # ✅ Final evaluation summary if completed
    if st.session_state.completed:
        if st.session_state.evaluation_results:
            total_score = sum(result['score'] for result in st.session_state.evaluation_results)
            avg_score = total_score / len(st.session_state.evaluation_results)

            summary = f"""
**Interview Complete! 🎯**

**Final Evaluation:**
- Total Questions: {len(st.session_state.evaluation_results)}
- Average Score: {avg_score:.1f}/10
- Overall Performance: {'Excellent' if avg_score >= 8 else 'Good' if avg_score >= 6 else 'Needs Improvement' if avg_score >= 4 else 'Poor'}

**Detailed Results:**
"""
            for i, result in enumerate(st.session_state.evaluation_results):
                summary += f"\n**Question {i + 1}:** {result['question'][:50]}...\n"
                summary += f"**Score:** {result['score']}/10\n"
                summary += f"**Feedback:** {result['feedback']}\n"

            message(summary, is_user=False, key="final_summary")

        message(
            "Thank you for your time! Your interview results have been recorded. Our team will contact you soon.",
            is_user=False,
            key="completed_message"
        )
        return

    # ✅ Phase 1: Collect candidate information
    if not st.session_state.interview_mode and st.session_state.step < len(info_questions):
        key, label = info_questions[st.session_state.step]
        prompt = info_prompt(label)
        message(prompt, is_user=False, key=f"prompt_{st.session_state.step}")
        user_input = st.text_input("Your response:", key=f"input_{key}_{st.session_state.step}")

        if user_input:
            if is_exit(user_input):
                message("Session ended. Goodbye!", is_user=False, key=f"exit_{st.session_state.step}")
                st.session_state.completed = True
                return

            # Validate input
            user_input = sanitize_input(user_input)
            valid = True
            if key == "email":
                valid = validate_email(user_input)
            elif key == "phone":
                valid = validate_phone(user_input)
            elif key == "experience":
                try:
                    user_input = int(user_input)
                    valid = user_input >= 0
                except Exception:
                    valid = False
            elif key == "tech_stack":
                user_input = [tech.strip() for tech in user_input.split(",") if tech.strip()]
                valid = bool(user_input)

            if not valid:
                fallback = fallback_prompt(label)
                message(fallback, is_user=False, key=f"fallback_{st.session_state.step}")
                st.stop()

            # Save response
            st.session_state.candidate[key] = user_input
            st.session_state.chat_history.append({"message": prompt, "is_user": False})
            st.session_state.chat_history.append({"message": str(user_input), "is_user": True})
            st.session_state.step += 1
            st.rerun()

    # ✅ Phase 2: Confirm details and start interview
    elif not st.session_state.interview_mode and st.session_state.step >= len(info_questions):
        summary = "Here are the details you provided:\n" + "\n".join([
            f"**{label}:** {st.session_state.candidate[key] if key != 'tech_stack' else ', '.join(st.session_state.candidate[key])}"
            for key, label in info_questions
        ])
        message(summary, is_user=False, key=f"summary_{len(st.session_state.chat_history)}")

        if st.button("Start Technical Interview", key="start_interview"):
            questions_list = generate_questions(st.session_state.candidate["tech_stack"])
            if questions_list and not questions_list[0].startswith("Error"):
                st.session_state.interview_questions = questions_list
                st.session_state.interview_mode = True
                st.session_state.current_question_index = 0
                st.session_state.chat_history.append({"message": summary, "is_user": False})
                st.session_state.chat_history.append({
                    "message": "Great! Let's start your technical interview. I'll ask you questions one by one and evaluate your answers.",
                    "is_user": False
                })
                st.rerun()
            else:
                st.session_state.chat_history.append({
                    "message": "Sorry, there was an error generating questions. Please try again later.",
                    "is_user": False
                })
                st.rerun()

    # ✅ Phase 3: Interactive interview
    elif st.session_state.interview_mode:
        if st.session_state.current_question_index < len(st.session_state.interview_questions):
            current_question = st.session_state.interview_questions[st.session_state.current_question_index]
            question_prompt = f"**Question {st.session_state.current_question_index + 1}:** {current_question}"
            message(question_prompt, is_user=False, key=f"question_{st.session_state.current_question_index}")

            # Candidate answer
            user_answer = st.text_area(
                "Your answer:",
                key=f"answer_{st.session_state.current_question_index}",
                height=150
            )

            if st.button("Submit Answer", key=f"submit_{st.session_state.current_question_index}"):
                if user_answer.strip():
                    evaluation = evaluate_answer(current_question, user_answer)
                    st.session_state.evaluation_results.append({
                        'question': current_question,
                        'answer': user_answer,
                        'score': evaluation['score'],
                        'feedback': evaluation['feedback']
                    })

                    # Append chat history
                    st.session_state.chat_history.append({"message": question_prompt, "is_user": False})
                    st.session_state.chat_history.append({"message": user_answer, "is_user": True})
                    st.session_state.chat_history.append(
                        {"message": f"**Score: {evaluation['score']}/10**", "is_user": False})
                    st.session_state.chat_history.append(
                        {"message": f"**Feedback:** {evaluation['feedback']}", "is_user": False})

                    st.session_state.current_question_index += 1
                    st.rerun()
                else:
                    st.error("Please provide an answer before submitting.")
        else:
            st.session_state.completed = True
            st.rerun()


if __name__ == "__main__":
    main()
