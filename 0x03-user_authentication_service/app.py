#!/usr/bin/env python3
"""seting minimal flask app"""
from flask import Flask
from flask import request
from flask import jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
