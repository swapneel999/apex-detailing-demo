import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)
DB_PASSWORD = os.getenv("DB_PASSWORD")

@app.route('/get_user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = str(cursor.fetchall())
    conn.close()
    return result