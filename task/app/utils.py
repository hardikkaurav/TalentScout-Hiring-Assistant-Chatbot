"""
Helper functions for validation, saving, and input handling.
"""
import re
import json
import os
from typing import Any, Dict

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None

def sanitize_input(text: str) -> str:
    return text.strip()

def save_candidate_info(candidate: Dict[str, Any], path: str = None) -> None:
    """Save candidate info to data/candidates.json."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "candidates.json")
    path = os.path.abspath(path)
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
    else:
        data = []
    data.append(candidate)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def handle_fallback(field_label: str) -> str:
    return f"Input for {field_label} was not valid. Please try again."
