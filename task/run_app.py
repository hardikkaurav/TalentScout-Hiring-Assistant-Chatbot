#!/usr/bin/env python3
"""
Startup script for TalentScout Hiring Assistant Chatbot.
Handles environment setup and launches the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("📝 Creating .env file from template...")
        
        # Copy from env.example if it exists
        example_file = Path("env.example")
        if example_file.exists():
            with open(example_file, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env file created from template")
            print("🔑 Please edit .env file and add your GEMINI_API_KEY")
            return False
        else:
            print("❌ env.example not found. Please create .env file manually.")
            return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("⚠️  GEMINI_API_KEY not set in .env file")
        print("🔑 Please add your Gemini API key to the .env file")
        return False
    
    print("✅ Environment check passed")
    return True

def run_streamlit():
    """Run the Streamlit application."""
    print("\n🚀 Starting Streamlit application...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app/main.py",
            "--server.headless", "true",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        return False
    return True

def run_api():
    """Run the FastAPI backend."""
    print("\n🚀 Starting FastAPI backend...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app.api:app",
            "--reload",
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 API stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running FastAPI: {e}")
        return False
    return True

def main():
    """Main function."""
    print("🎯 TalentScout Hiring Assistant Startup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup incomplete. Please fix the issues above.")
        sys.exit(1)
    
    # Ask user what to run
    print("\n📋 What would you like to run?")
    print("1. Streamlit Web App (recommended)")
    print("2. FastAPI Backend")
    print("3. Both (in separate terminals)")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_streamlit()
            break
        elif choice == "2":
            run_api()
            break
        elif choice == "3":
            print("🔄 Starting both applications...")
            print("📱 Streamlit will be available at: http://localhost:8501")
            print("🔌 API will be available at: http://localhost:8000")
            print("📖 API docs at: http://localhost:8000/docs")
            
            # Start API in background
            api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "app.api:app",
                "--reload", "--port", "8000"
            ])
            
            try:
                # Start Streamlit
                run_streamlit()
            finally:
                # Clean up API process
                api_process.terminate()
                api_process.wait()
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 