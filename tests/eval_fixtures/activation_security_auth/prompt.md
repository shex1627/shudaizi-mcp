Can you finish this login/registration module? The signup part works but
I haven't done the login yet. Also the password stuff is probably wrong,
I just stored it as-is for now to get the tests passing.

```python
"""User auth module for the Flask app."""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "users.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()
    db.execute(
        f"INSERT INTO users (email, password, name) VALUES ('{data['email']}', '{data['password']}', '{data['name']}')"
    )
    db.commit()
    return jsonify({"status": "created"}), 201


@app.route("/login", methods=["POST"])
def login():
    # TODO: implement login
    pass
```

Just need basic email/password login that returns some kind of token.
Don't overthink it, just something that works for our MVP.
