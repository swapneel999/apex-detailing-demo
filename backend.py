import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/get_user')
def get_user():
    user_id = request.args.get('id')

    # Validate user_id to ensure it's an integer, preventing non-integer inputs
    # from reaching the database query and potentially causing errors or unexpected behavior.
    if not user_id or not user_id.isdigit():
        return "Invalid user ID", 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # FIX: Use a parameterized query to prevent SQL Injection.
    # The '?' acts as a placeholder for the user_id.
    # The database driver (sqlite3 in this case) will properly escape the value,
    # ensuring that it is treated as data and not as executable SQL code.
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,)) # Pass user_id as a tuple for the parameter
    
    result = cursor.fetchall()
    conn.close() # Close the database connection
    return str(result)