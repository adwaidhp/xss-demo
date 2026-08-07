from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "blog.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/comments", methods=["GET"])
def get_comments():
    conn = get_db()
    rows = conn.execute("SELECT * FROM comments ORDER BY created_at ASC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/comments", methods=["POST"])
def post_comment():
    data = request.get_json()
    name = data.get("name", "").strip()
    body = data.get("body", "").strip()
    if not name or not body:
        return jsonify({"error": "name and body required"}), 400
    conn = get_db()
    conn.execute("INSERT INTO comments (name, body) VALUES (?, ?)", (name, body))
    conn.commit()
    conn.close()
    return jsonify({"ok": True}), 201

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
