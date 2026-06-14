import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
# DB_PASSWORD = "super_secret_db_password_123!" # Hardcoded secret removed

@app.route('/get_user')
def get_user():
    user_id_str = request.args.get('id')
    
    if not user_id_str:
        return jsonify({"error": "User ID is required"}), 400
    
    try:
        user_id = int(user_id_str)
        if user_id < 1: # Basic validation for positive IDs
            return jsonify({"error": "Invalid User ID"}), 400
    except ValueError:
        return jsonify({"error": "Invalid User ID format"}), 400

    conn = None
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        
        user_data = cursor.fetchall()
        
        if not user_data:
            return jsonify({"message": "User not found"}), 404
            
        return jsonify(user_data)
    
    except sqlite3.Error:
        return jsonify({"error": "An internal server error occurred"}), 500
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500
    finally:
        if conn:
            conn.close()