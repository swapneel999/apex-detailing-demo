import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)
DB_PASSWORD = os.getenv("DB_PASSWORD") # Replaced hardcoded password with os.getenv()

@app.route('/get_user')
def get_user():
    user_id = request.args.get('id')
    
    # Basic validation to ensure user_id is not None, though not strictly required by the prompt for the fix
    if user_id is None:
        return "Error: 'id' parameter is missing", 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Using a parameterized query to prevent SQL Injection
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,)) # user_id is passed as a parameter
    
    result = cursor.fetchall()
    conn.close() # Close the connection
    return str(result)