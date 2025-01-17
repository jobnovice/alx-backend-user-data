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
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
