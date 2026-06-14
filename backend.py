import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
# DB_PASSWORD was hardcoded and is removed as per "Hardcoded Secrets" vulnerability.
# If a database password were required, it would be loaded via os.getenv("DB_PASSWORD").

@app.route('/get_user')
def get_user():
    user_id_str = request.args.get('id')

    # 3. Add input validation and type checking
    if not user_id_str:
        return jsonify({"error": "User ID is required"}), 400

    try:
        user_id = int(user_id_str)
        # Basic validation: ensure ID is positive
        if user_id <= 0:
            return jsonify({"error": "Invalid User ID"}), 400
    except ValueError:
        return jsonify({"error": "User ID must be an integer"}), 400

    conn = None
    cursor = None
    try:
        # Establish database connection
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # 1. Use parameterized SQL queries to prevent SQL Injection
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchall()

        # Return data as string, matching the original output format
        return str(user_data)

    except sqlite3.Error as e:
        # 5. Add error handling without exposing sensitive info
        # Log the actual error for internal debugging purposes
        print(f"Database error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        # 4. Ensure proper resource cleanup (close connections in finally blocks)
        if cursor:
            cursor.close()
        if conn:
            conn.close()