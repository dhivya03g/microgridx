from flask import Flask, jsonify, request, session, redirect, send_from_directory
from flask_cors import CORS
import os
import sys

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from decision_layer.decision_engine import run_decision_engine

app = Flask(__name__)
CORS(app)

# 🔐 Secret key for login
app.secret_key = "microgrid_secret"

# 👤 Demo user
USER = {
    "username": "admin",
    "password": "1234"
}

# 🌐 HOME
@app.route("/")
def home():
    return redirect("/login")

# 🔐 LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "❌ Invalid Credentials"

    return """
    <h2>⚡ MicroGridX Login</h2>
    <form method="POST">
        <input name="username" placeholder="Username"/><br><br>
        <input name="password" type="password" placeholder="Password"/><br><br>
        <button type="submit">Login</button>
    </form>
    """

# 🔓 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# 📊 DASHBOARD (Protected)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "../digital-twin"),
        "index.html"
    )

# 🔥 API
@app.route("/api/data")
def get_data():
    try:
        result = run_decision_engine()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)