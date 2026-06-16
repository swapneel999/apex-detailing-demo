#!/usr/bin/env python3
"""
Lead Generation API - Vulnerable Version for Testing
This backend intentionally contains security vulnerabilities for CI/CD auditor validation.
"""

import sqlite3
import json
import os
import re
from flask import Flask, request, jsonify

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
# Removed hardcoded fallback for STRIPE_SECRET_KEY.
# If not set, STRIPE_SECRET_KEY will be None, requiring proper environment configuration.

DATABASE = "leads.db"

app = Flask(__name__)

def init_db():
    """Initialize SQLite database if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
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
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

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

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format, expected an object"}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all(isinstance(arg, str) and arg.strip() for arg in [name, email, message]):
            return jsonify({"error": "Missing or invalid required fields (name, email, message must be non-empty strings)"}), 400

        name = name.strip()
        email = email.strip()
        message = message.strip()

        if not EMAIL_REGEX.match(email):
            return jsonify({"error": "Invalid email format"}), 400

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
        return jsonify({"error": "Invalid JSON payload"}), 400
    except sqlite3.Error as e:
        print(f"Database error processing contact form: {e}")
        return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        print(f"Unexpected error processing contact form: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
        return jsonify({"status": "ok", "database": "connected"}), 200
    except sqlite3.Error:
        return jsonify({"status": "degraded", "database": "disconnected"}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=os.getenv("FLASK_DEBUG") == "True", host='0.0.0.0', port=5000)