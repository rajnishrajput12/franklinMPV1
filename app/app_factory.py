import os
from flask import Flask
from app.models import load_users
from app.search import SearchEngine
from app.data_loader import load_app_data, load_reviews
from flask_login import LoginManager
from app.auth import User

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Load users (in-memory)
    app.users = load_users()

    # Load app data
    app.apps_df = load_app_data()
    app.reviews_df = load_reviews()
    
    # Initialize search engine (BERT-based)
    app.search_engine = SearchEngine(app.apps_df)

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        user_obj = app.users.get(username)
        return User(username, user_obj["role"]) if user_obj else None

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.search import search_bp
    from app.routes.reviews import reviews_bp
    from app.routes.supervisor import supervisor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(supervisor_bp)

    return app