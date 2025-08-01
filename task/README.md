# TalentScout Hiring Assistant Chatbot

## Project Overview
A Streamlit-based chatbot for initial candidate screening, used by a fictional recruitment agency. It collects candidate information and generates technical questions based on the candidate’s tech stack.

## Setup & Installation Instructions
1. Clone the repository or copy the `task/` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key in a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
4. **Easy way**: Run the startup script:
   ```bash
   python run_app.py
   ```
5. **Manual way**: Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```
6. (Optional) Run the FastAPI backend:
   ```bash
   uvicorn app.api:app --reload
   ```

## How to Use
- Launch the app and follow the chat prompts to enter your details.
- The chatbot will confirm your information and generate technical questions.
- Type `exit` or `bye` to end the conversation at any time.

## Prompt Design Strategy
- **One-shot prompting** for data collection.
- **Chain-of-thought prompting** for technical question generation.
- Fallback prompts for invalid or off-topic input.

## Challenges & Solutions
- **Input validation:** Regex and type checks for email, phone, and experience.
- **LLM reliability:** Fallback to raw output if parsing fails.
- **User experience:** Chat-style UI and clear error handling.

## Tech Stack Used
- Streamlit, streamlit-chat
- Google Gemini API
- FastAPI, Pydantic, Uvicorn
- Python-dotenv, httpx

## Testing
Run the comprehensive test suite:
```bash
python test_app.py
```

## Demo Link or MP4
See `demo.mp4` or `link.txt` in the project root for a walkthrough.
