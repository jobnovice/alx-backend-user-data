#!/usr/bin/env python3
"""New view for Session Authentication"""
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify
import os
from flask import session


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def sessh_view():
    """handles all the routes for
        the session authentication
    """
    email = request.form.get('email')
    passw = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not passw:
        return jsonify({"error": "password missing"}), 400
    usr = User.search({"email": email})
    if not usr or len(usr) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    usr = usr[0]  # Retrieve the first user found
    if not usr.is_valid_password(passw):
        return jsonify({"error": "wrong password"}), 401

    # Import `auth` dynamically to avoid circular imports
    from api.v1.app import auth

    # Create session and set the session cookie
    ssid = auth.create_session(usr.id)
    session_name = os.environ.get('SESSION_NAME', '_my_session_id')
    response = jsonify(usr.to_json())
    response.set_cookie(session_name, ssid)

    return response
