from functools import wraps
from flask import request, abort, g
from app.profile.utils import normalize_keys

def validate_input(accepted_keys):
    """
    Middleware-like decorator to validate and normalize request input.
    params:
        - accepted_keys: list of allowed keys for the API endpoint
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            data = request.get_json() if request.is_json else request.form.to_dict()

            if not data:
                abort(400, description = "No input provided")

            try:
                normalized = normalize_keys(data, to = "snake")

            except ValueError as e:
                abort(400, description = str(e))

            filtered = {k: v.strip() for k, v in normalized.items() if k in accepted_keys}

            if not filtered:
                abort(400, description = "No valid fields provided")

            g.normalized_data = filtered

            return fn(*args, **kwargs)
        
        return wrapper
    
    return decorator
