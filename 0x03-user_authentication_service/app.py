#!/usr/bin/env python3
"""seting minimal flask app"""
from flask import Flask
from flask import request
from flask import jsonify, make_response
from flask import abort, redirect, url_for
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def hello():
    """simple binevenue message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """register user based on the credential sent"""
    try:
        user = AUTH.register_user(request.form['email'],
                                  request.form['password'])
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{request.form['email']}",
                    "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """logins based on it's credentials"""
    email = request.form['email']
    valid = AUTH.valid_login(email, request.form['password'])
    if valid:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirects to home route.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not session_id or not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=["GET"])
def profile():
    """looks for a particular user respond with it's email"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not session_id or not user:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', methods=["POST"])
def get_reset_password_token():
    """resets the password of the user"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}",
                    "reset_token": f"{reset_token}"})


@app.route('/update_password', methods=["PUT"])
def update_password():
    """updates the user password by checking if first if
    the user has the right reset_token"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
