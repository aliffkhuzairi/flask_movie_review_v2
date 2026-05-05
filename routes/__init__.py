from .auth_routes import auth_bp
from .movie_routes import movie_bp
from .user_routes import user_bp
from .search_routes import search_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(search_bp)