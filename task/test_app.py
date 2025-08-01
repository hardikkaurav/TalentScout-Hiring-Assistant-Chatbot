#!/usr/bin/env python3
"""
Comprehensive test script for TalentScout Hiring Assistant Chatbot.
Tests all modules and functionality.
"""

import os
import sys
import json
from unittest.mock import patch, MagicMock

def test_imports():
    """Test all module imports."""
    print("Testing imports...")
    try:
        import streamlit
        from streamlit_chat import message
        import openai
        import fastapi
        import pydantic
        import uvicorn
        import httpx
        from dotenv import load_dotenv
        print("✓ All external imports successful")
        
        from app.utils import validate_email, validate_phone, sanitize_input, save_candidate_info
        from app.prompts import info_prompt, question_prompt, fallback_prompt
        from app.question_generator import generate_questions
        from app.main import main
        from app.api import app
        print("✓ All app imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_validation_functions():
    """Test validation functions."""
    print("\nTesting validation functions...")
    try:
        from app.utils import validate_email, validate_phone, sanitize_input
        
        # Test email validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        assert validate_email("test@domain.co.uk") == True
        print("✓ Email validation working")
        
        # Test phone validation
        assert validate_phone("+1234567890") == True
        assert validate_phone("1234567890") == True
        assert validate_phone("invalid") == False
        print("✓ Phone validation working")
        
        # Test sanitize input
        assert sanitize_input("  test  ") == "test"
        print("✓ Input sanitization working")
        
        return True
    except Exception as e:
        print(f"✗ Validation test error: {e}")
        return False

def test_prompts():
    """Test prompt functions."""
    print("\nTesting prompts...")
    try:
        from app.prompts import info_prompt, question_prompt, fallback_prompt
        
        # Test info prompt
        prompt = info_prompt("Name")
        assert "Name" in prompt
        print("✓ Info prompt working")
        
        # Test question prompt
        q_prompt = question_prompt(["Python", "Django"])
        assert "Python" in q_prompt and "Django" in q_prompt
        print("✓ Question prompt working")
        
        # Test fallback prompt
        f_prompt = fallback_prompt("Email")
        assert "Email" in f_prompt
        print("✓ Fallback prompt working")
        
        return True
    except Exception as e:
        print(f"✗ Prompt test error: {e}")
        return False

def test_question_generator():
    """Test question generator with mock API."""
    print("\nTesting question generator...")
    try:
        from app.question_generator import generate_questions
        
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": "1. What is Python?\n2. How does Django work?\n3. Explain ORM."}]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.post', return_value=mock_response):
            questions = generate_questions(["Python", "Django"])
            assert len(questions) > 0
            print("✓ Question generator working with mock API")
        
        # Test without API key
        with patch.dict(os.environ, {}, clear=True):
            questions = generate_questions(["Python"])
            assert "Error" in questions[0]
            print("✓ Question generator handles missing API key")
        
        return True
    except Exception as e:
        print(f"✗ Question generator test error: {e}")
        return False

def test_data_saving():
    """Test candidate data saving."""
    print("\nTesting data saving...")
    try:
        from app.utils import save_candidate_info
        import tempfile
        import os
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        # Test data
        test_candidate = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "experience": 3,
            "position": "Developer",
            "location": "Test City",
            "tech_stack": ["Python", "Django"]
        }
        
        # Save data
        save_candidate_info(test_candidate, temp_file)
        
        # Verify data was saved
        with open(temp_file, 'r') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["name"] == "Test User"
        
        # Cleanup
        os.unlink(temp_file)
        print("✓ Data saving working")
        
        return True
    except Exception as e:
        print(f"✗ Data saving test error: {e}")
        return False

def test_api_endpoints():
    """Test FastAPI endpoints."""
    print("\nTesting API endpoints...")
    try:
        from app.api import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test generate questions endpoint
        response = client.post("/generate_questions", json={"tech_stack": ["Python"]})
        assert response.status_code in [200, 400]  # 400 if no API key
        print("✓ Generate questions endpoint working")
        
        # Test save candidate endpoint
        candidate_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "experience": 3,
            "position": "Developer",
            "location": "Test City",
            "tech_stack": ["Python", "Django"],
            "questions": []
        }
        response = client.post("/save_candidate", json=candidate_data)
        assert response.status_code == 200
        print("✓ Save candidate endpoint working")
        
        return True
    except Exception as e:
        print(f"✗ API test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Starting comprehensive tests for TalentScout Hiring Assistant...\n")
    
    tests = [
        test_imports,
        test_validation_functions,
        test_prompts,
        test_question_generator,
        test_data_saving,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo run the application:")
        print("1. Copy env.example to .env and add your GEMINI_API_KEY")
        print("2. Run: streamlit run app/main.py")
        print("3. Or run the API: uvicorn app.api:app --reload")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 