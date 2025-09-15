from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import User

    # blueprints
    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix = "/api/users")


    from app.profile.consumer import run_consumer
    @app.cli.command("worker")
    @with_appcontext
    def worker():
        """Start the email queue consumer."""
        run_consumer(app = app)

    return app