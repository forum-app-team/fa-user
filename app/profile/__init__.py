from flask import Blueprint

profile_bp = Blueprint("user_profile", __name__)

from . import routes, views

