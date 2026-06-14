import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)
db_password = os.getenv("DB_PASSWORD")

@app.route('/get_user')
def get_user():
    user_id = request.args.get('id')
    
    if not user_id:
        return "User ID is required", 400
    
    try:
        user_id_int = int(user_id) 
    except ValueError:
        return "Invalid User ID format", 400

    conn = None
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id_int,))
        
        result = cursor.fetchall()
        return str(result)
    finally:
        if conn:
            conn.close()