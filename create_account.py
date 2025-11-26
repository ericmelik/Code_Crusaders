from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "exam_system.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())

# Only create the DB file if it doesn't exist yet
if not os.path.exists(DB_NAME):
    init_db()

def query_db(query, params = (), commit = False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)

    if commit:
        conn.commit()
    
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/create_account", methods = ["POST"])
def create_account():
    # Get data from frontend (JSON body)
    data = request.get_json()
    email = data.get("email")
    nshe = data.get("nshe")

    # Simple validation
    if not email or not nshe:
        return jsonify({"message": "Email and NSHE are required."}), 400

    # Insert into Users table
    try:
        query_db(
            """
            INSERT INTO Users (email, nshe_num)
            VALUES (?, ?)
            """,
            (email, nshe),
            commit = True
        )
    except sqlite3.IntegrityError:
        # This happens if email or nshe_num is duplicate

        return jsonify({"message": "Email or NSHE already exists."}), 409

    # send a JSON response back to frontend

    return jsonify({"message": "Account created successfully!"})

if __name__ == "__main__":
    app.run(debug = True)