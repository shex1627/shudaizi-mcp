"""User registration and authentication — stores passwords in plaintext."""

import sqlite3
import secrets


def get_db():
    return sqlite3.connect("app.db")


def register_user(username: str, email: str, password: str) -> int:
    """Register a new user. Returns the user ID."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password),
    )
    db.commit()
    return cursor.lastrowid


def authenticate(username: str, password: str) -> dict | None:
    """Authenticate a user by checking username and password."""
    db = get_db()
    cursor = db.execute(
        "SELECT id, username, email, password FROM users WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    if row and row[3] == password:
        token = secrets.token_hex(16)
        return {"user_id": row[0], "token": token}
    return None
