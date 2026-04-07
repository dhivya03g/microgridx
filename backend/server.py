from flask import Flask, jsonify, request, session, redirect, send_from_directory
from flask_cors import CORS
import os
import sys
import json

# 🔥 NEW (for encryption)
from werkzeug.security import generate_password_hash, check_password_hash

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decision_layer.decision_engine import run_decision_engine

# 🔥 Serve frontend
app = Flask(__name__, static_folder='../digital-twin', static_url_path='')
CORS(app)

# 🔐 Secret key
app.secret_key = "microgrid_secret"

# =========================
# 🧠 USER DATABASE FUNCTIONS
# =========================

USER_FILE = "data/users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# =========================
# 🌐 HOME → LOGIN PAGE
# =========================

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")

# =========================
# 🔐 SIGNUP
# =========================

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    # check if user exists
    for u in users:
        if u["username"] == username:
            return jsonify({"status": "fail", "message": "User already exists"})

    # 🔥 NEW (hash password)
    hashed_password = generate_password_hash(password)

    users.append({
        "username": username,
        "password": hashed_password
    })

    save_users(users)

    return jsonify({"status": "success"})

# =========================
# 🔐 LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    for u in users:
        # 🔥 MODIFIED (secure check)
        if u["username"] == username and check_password_hash(u["password"], password):
            session["user"] = username
            return jsonify({"status": "success"})

    return jsonify({"status": "fail", "message": "Invalid Credentials"})

# =========================
# 🔓 LOGOUT
# =========================

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# =========================
# 📊 DASHBOARD (Protected)
# =========================

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return send_from_directory(app.static_folder, "index.html")

# =========================
# 📡 API DATA
# =========================

@app.route("/api/data")
def get_data():
    try:
        result = run_decision_engine()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

# =========================
# 📁 ADDITION (STATIC JS ROUTE)
# =========================

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)