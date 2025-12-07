from flask import Blueprint, request, jsonify, session
from am.models.users_model import create_user, login_user

auth_bp = Blueprint("auth_bp", __name__)

# -----------------------------
# Register Route
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    result = create_user(email, password)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


# -----------------------------
# Login Route
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required!"}), 400

    result = login_user(email, password)

    if "error" in result:
        return jsonify(result), 401

    # ✅ Save user in session
    session["user_id"] = result["user_id"]
    return jsonify(result), 200


# -----------------------------
# Logout Route
# -----------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"msg": "Logged out successfully!"}), 200
