import jwt
from flask import request, g, jsonify, abort
from functools import wraps

from config import Config

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        
        if not auth_header or not auth_header.startswith("Bearer "):
            # return jsonify({"message": "Missing or invalid token in the header"}), 401
            abort(401, description = "Missing or invalid token in the header")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, Config.JWT_ACCESS_SECRET, algorithms=["HS256"])
            g.user_id = payload.get("sub")
            g.role = payload.get("role", "normal")

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            # return jsonify({"message": "Invalid or expired expired"}), 401
            abort(401, description = "Invalid or expired token")

        return f(*args, **kwargs)
    return decorated
