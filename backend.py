#!/usr/bin/env python3
"""
Lead Generation API - Vulnerable Version for Testing
This backend intentionally contains security vulnerabilities for CI/CD auditor validation.
"""

import sqlite3
import json
import os
import re # For email validation
from flask import Flask, request, jsonify

# VULNERABILITY 1: Hardcoded Secret Key -> FIXED: Load from environment
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if not STRIPE_SECRET_KEY:
    print("WARNING: STRIPE_SECRET_KEY environment variable not set.")
    # In a production environment, you might want to raise an error or exit here.

# VULNERABILITY 2: DATABASE path could also be an environment variable
DATABASE = os.getenv("DATABASE_PATH", "leads.db")

app = Flask(__name__)

# Basic email regex for validation
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def init_db():
    """Initialize SQLite database if it doesn't exist."""
    # VULNERABILITY 3: Potential Database Connection Leak -> FIXED with 'with' statement
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        # Depending on the application, you might want to exit or handle this more gracefully.

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """
    Receive lead generation form submissions.

    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Interested in your service"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # VULNERABILITY 4: Insufficient Input Validation -> FIXED: Add input validation and type checking
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Type checking
        if not all(isinstance(field, str) for field in [name, email, message]):
            return jsonify({"error": "All fields (name, email, message) must be strings"}), 400

        # Presence and length validation
        if not name or not email or not message:
            return jsonify({"error": "Missing required fields (name, email, message)"}), 400

        if not (1 <= len(name) <= 100):
            return jsonify({"error": "Name must be between 1 and 100 characters"}), 400
        if not (1 <= len(email) <= 255):
            return jsonify({"error": "Email must be between 1 and 255 characters"}), 400
        if not (1 <= len(message) <= 1000):
            return jsonify({"error": "Message must be between 1 and 1000 characters"}), 400

        # Email format validation
        if not EMAIL_REGEX.match(email):
            return jsonify({"error": "Invalid email format"}), 400

        # VULNERABILITY 2: SQL Injection via String Concatenation -> FIXED: Use parameterized SQL queries
        # VULNERABILITY 3: Potential Database Connection Leak -> FIXED with 'with' statement
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            query = "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
            cursor.execute(query, (name, email, message))
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Lead captured successfully"
        }), 201

    except json.JSONDecodeError:
        # VULNERABILITY 5: Add error handling without exposing sensitive info
        return jsonify({"error": "Invalid JSON format"}), 400
    except sqlite3.Error as db_error:
        # VULNERABILITY 5: Add error handling without exposing sensitive info
        print(f"Database error processing contact form: {db_error}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        # VULNERABILITY 5: Add error handling without exposing sensitive info
        print(f"Unexpected error processing contact form: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    init_db()
    # In a production environment, debug=True should be disabled.
    # Also, consider using a production-ready WSGI server like Gunicorn.
    app.run(debug=False, host='0.0.0.0', port=5000)