#!/usr/bin/env python3
""" Session Authentication views Module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    not_found_error = {"error": "no user found for this email"}
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email.strip()) == 0:
        return jsonify({'error': 'email missing'}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({'error': 'password missing'}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_error), 404
    if len(users) <= 0:
        return jsonify(not_found_error), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0].id))
        cookie_name = getenv('SESSION_NAME')
        response = jsonify(users[0].to_json())
        response.set_cookie(cookie_name, session_id)
        return response
    return jsonify({'error': 'wrong password'}), 404

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON
    """
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200