#!/usr/bin/env python3
"""
Lead Generation API - Fixed Version
This backend has been patched to address identified security vulnerabilities.
"""

import sqlite3
import json
import os
from flask import Flask, request, jsonify

# Load secret key from environment variable
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
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
                email TEXT,
                name TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        # Depending on the application, you might want to re-raise or exit here
    finally:
        if conn:
            conn.close()


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
    conn = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Input validation and type checking
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all(isinstance(field, str) and field for field in [name, email, message]):
            return jsonify({"error": "Missing or invalid required fields (name, email, message)"}), 400

        # Basic email format check (can be more robust with regex)
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # SQL Injection fix: Use parameterized query
        query = "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)"
        cursor.execute(query, (name, email, message))
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Lead captured successfully"
        }), 201

    except sqlite3.Error as e:
        print(f"Database error processing contact form: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        print(f"Error processing contact form: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        # Ensure proper resource cleanup
        if conn:
            conn.close()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    init_db()
    # Insecure Configuration fix: Do not run with debug=True in production
    # Use an environment variable for debug mode, defaulting to False
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)