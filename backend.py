import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)
DB_PASSWORD = os.getenv("DB_PASSWORD")

@app.route('/get_user')
def get_user():
    user_id_str = request.args.get('id')

    if not user_id_str:
        return "User ID is required", 400

    try:
        user_id = int(user_id_str)
    except ValueError:
        return "Invalid user ID format", 400

    conn = None
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Use parameterized queries to prevent SQL injection
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return str(result)
    except sqlite3.Error as e:
        # Log the error internally for debugging, but return a generic message to the client
        print(f"Database error: {e}")
        return "An internal server error occurred", 500
    finally:
        if conn:
            conn.close()