"""User search endpoint — vulnerable to SQL injection."""

import sqlite3


def get_db():
    return sqlite3.connect("app.db")


def search_users(query: str) -> list[dict]:
    """Search users by name."""
    db = get_db()
    cursor = db.execute(f"SELECT id, name, email FROM users WHERE name LIKE '%{query}%'")
    results = []
    for row in cursor.fetchall():
        results.append({"id": row[0], "name": row[1], "email": row[2]})
    return results


def get_user_orders(user_id: str) -> list[dict]:
    """Fetch orders for a given user."""
    db = get_db()
    cursor = db.execute(
        "SELECT id, total, status FROM orders WHERE user_id = " + user_id
    )
    return [{"id": r[0], "total": r[1], "status": r[2]} for r in cursor.fetchall()]
