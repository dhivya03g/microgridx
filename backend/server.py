from flask import Flask, jsonify, request, session, redirect, send_from_directory
from flask_cors import CORS
import os
import sys

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decision_layer.decision_engine import run_decision_engine

# 🔥 IMPORTANT (serve frontend)
app = Flask(__name__, static_folder='../digital-twin', static_url_path='')
CORS(app)

# 🔐 Secret key
app.secret_key = "microgrid_secret"

# 👤 Demo user
USER = {
    "username": "admin",
    "password": "1234"
}

# 🌐 HOME → LOGIN PAGE
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "login.html")


# 🔐 LOGIN API (ONLY POST)
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username == USER["username"] and password == USER["password"]:
        session["user"] = username
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail", "message": "Invalid Credentials"})


# 🔓 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return send_from_directory(app.static_folder, "index.html")


# 📡 API DATA
@app.route("/api/data")
def get_data():
    try:
        result = run_decision_engine()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)