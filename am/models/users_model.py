import sqlite3
from am.db import get_db

def create_user(email, password):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        return {"error": "Email already exists"}

    cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    db.commit()
    return {"msg": "User registered successfully!"}

def login_user(email, password):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    if not user:
        return {"error": "Email not found!"}
    if user["password"] != password:
        return {"error": "Incorrect password!"}

    return {"msg": "Login successful!", "user_id": user["id"]}
