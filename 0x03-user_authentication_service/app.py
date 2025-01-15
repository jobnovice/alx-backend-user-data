#!/usr/bin/env python3
"""seting minimal flask app"""
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
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
        AUTH.create_session(email)
        return jsonify({"email": f"{email}", "message": "logged in"})
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
