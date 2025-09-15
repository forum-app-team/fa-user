from flask import request, jsonify
from flask.views import MethodView

from . import profile_bp
from app import db
from app.models.User import User
from app.profile.utils import normalize_keys

# Mock db
USERS = {1: {"id": 1, "name": "Alice"}, 2: {"id": 2, "name": "Bob"}}

PROFILE_KEYS = ["first_name", "last_name", "profile_img_url"]

class UserProfileView(MethodView):
    def __init__(self):
        super().__init__()

    def dispatch_request(self, **kwargs):
        return super().dispatch_request(**kwargs)
    
    def get(self, user_id):
        '''
        Access existing profile. Incoming request args:
            - user_id: str, User ID (FK from Identity.id)
        '''
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        
        response = {
            "message": "Successfully acquired user profile",
            "profile": user.to_json()
            }
        return jsonify(response), 200


    def post(self):
        # create new profile
        # accepts msg from auth service upon user registration
        # Will not be necessary
        ...


    def patch(self, user_id):
        # Update existing profile

        '''Determine content type: 
            - JSON body (Content-Type: application/json)
            - Form data (application/x-www-form-urlencoded or multipart/form-data)
        '''
        data = request.get_json() if request.is_json else request.form.to_dict()

        if not user_id:
            return {"message": "Invalid user ID"}, 400
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        try:
            normalized_data = normalize_keys(data, to = "snake")
        except ValueError as e:
            return {"message": str(e)}, 400

        updated = False
        for key in PROFILE_KEYS:
            if key in normalized_data:

                # user[key] = normalized_data[key] // TypeError: 'User' object does not support item assignment
                setattr(user, key, normalized_data[key])
                
                updated = True
        
        if not updated:
            return {"message: No valid fields provided for update"}, 400
        
        db.session.commit()

        response = {
            "message": "Successfully updated user profile",
            "profile": user.to_json()
            }
        
        return jsonify(response), 200



profile_bp.add_url_rule(
    "/profile/<user_id>", 
    view_func = UserProfileView.as_view("user_profile"),
    methods = ["GET", "POST", "PATCH"]
    )
