from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from am.models.users_model import create_user, login_user

users_bp = Blueprint("users", __name__)

# -----------------------------
# 📄 صفحات HTML
# -----------------------------
@users_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@users_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

# -----------------------------
# 📌 تسجيل مستخدم جديد
# -----------------------------
@users_bp.route("/register", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    result = create_user(email, password)
    if "error" in result:
        return jsonify(result), 400

    return redirect(url_for("users.login_page"))

# -----------------------------
# 📌 تسجيل الدخول
# -----------------------------
@users_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    result = login_user(email, password)
    if "error" in result:
        return jsonify(result), 401

    # حفظ الـ session
    session["user_id"] = result["user_id"]
    return redirect(url_for("home"))

# -----------------------------
# 📌 تسجيل الخروج
# -----------------------------
@users_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
