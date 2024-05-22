#!/usr/bin/env python3
"""SessionAuth class that inherits from Auth."""
from api.v1.auth.auth import Auth
import uuid
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.__class__.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.__class__.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        Retrieves the User instance based on a cookie value.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        return User.get(user_id)
    

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if not session_id:
        abort(500)

    response = make_response(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response