#!/usr/bin/env python3
"""
Lead Generation API - Fixed Version
This backend has been patched to address critical security vulnerabilities.
"""

import sqlite3
import json
import os
from flask import Flask, request, jsonify

# VULNERABILITY 1 FIX: Load Secret Key from environment variables without hardcoded default
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY") # No hardcoded default allowed for secrets
DATABASE = os.getenv("DATABASE_PATH", "leads.db") # Also make database path configurable

app = Flask(__name__)


def init_db():
    """Initialize SQLite database if it doesn't exist."""
    # VULNERABILITY 3 FIX: Use context manager for database connection
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                email TEXT,
                name TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


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

        # REQ 3: Add input validation and type checking
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        required_fields = ['name', 'email', 'message']
        if not all(k in data for k in required_fields):
            missing = [f for f in required_fields if f not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        name = data['name']
        email = data['email']
        message = data['message']

        # Basic type checking
        if not isinstance(name, str) or not isinstance(email, str) or not isinstance(message, str):
            return jsonify({"error": "Name, email, and message must be strings"}), 400

        # Basic email format validation (can be enhanced with regex for production)
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # VULNERABILITY 2 FIX: SQL Injection prevented by parameterized query
        # VULNERABILITY 3 FIX: Use context manager for database connection
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # REQ 1: Use parameterized SQL queries
            query = "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
            cursor.execute(query, (name, email, message))
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Lead captured successfully"
        }), 201

    except Exception as e:
        # REQ 5: Add error handling without exposing sensitive info
        print(f"Error processing contact form: {e}") # Log the detailed error internally
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    init_db()
    # VULNERABILITY FIX: Set debug=False for production environments
    app.run(debug=False, host='0.0.0.0', port=5000)