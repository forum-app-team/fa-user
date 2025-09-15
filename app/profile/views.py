from flask import request, g, jsonify, abort
from flask.views import MethodView

from . import profile_bp
from app import db
from app.models.User import User
from app.profile.utils import normalize_keys
from app.middleware.jwt_middleware import jwt_required


PROFILE_KEYS = ["first_name", "last_name", "profile_img_url"]

class UserProfileView(MethodView):

    decorators = [jwt_required]

    def dispatch_request(self, **kwargs):
        return super().dispatch_request(**kwargs)
    
    def get(self, user_id):
        '''
        Access existing profile. Incoming request args:
            - user_id: str, User ID (FK from Identity.id)
        '''
        # If no user_id or "me", use current user
        if not user_id or user_id.lower() == "me":
            user_id = g.user_id

        user = db.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            abort(404, description = "User not found")
        
        if user_id != g.user_id:
            '''
            If we want to add restrictions later on viewing other users' profiles,
            implement it here. For now, it returns the whole profile page
            '''
            profile = user.to_json()
        else:
            profile = user.to_json()
        response = {
            "message": "Successfully acquired user profile",
            "profile": profile
            }
        return jsonify(response), 200


    def patch(self, user_id):
        # Update existing profile

        '''Determine content type: 
            - JSON body (Content-Type: application/json)
            - Form data (application/x-www-form-urlencoded or multipart/form-data)
        '''

        data = request.get_json() if request.is_json else request.form.to_dict()

        if not user_id:
            abort(400, description = "Invalid user ID")
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            abort(404, "User not found")
        
        # based on the requirement docs, a user cannot update someone else's profile
        # even if they are admins
        if g.user_id != user_id:
            abort(403, "Cannot change other users' profile")

        try:
            normalized_data = normalize_keys(data, to = "snake")
        except ValueError as e:
            abort(400, description = str(e))

        updated = False
        for key in PROFILE_KEYS:
            if key in normalized_data:
                new_val = normalized_data[key]
                curr_val =  getattr(user, key)

                if new_val != curr_val:
                    setattr(user, key, new_val)
                    updated = True
        
        if not updated:
            abort(400, description = "No changes detected")
        
        db.session.commit()

        response = {
            "message": "Successfully updated user profile",
            "profile": user.to_json()
            }
        
        return jsonify(response), 200


profile_bp.add_url_rule(
    "/profile/me",
    view_func=UserProfileView.as_view("my_profile"),
    methods=["GET"]
)

profile_bp.add_url_rule(
    "/profile/<user_id>", 
    view_func = UserProfileView.as_view("user_profile"),
    methods = ["GET", "PATCH"]
    )
