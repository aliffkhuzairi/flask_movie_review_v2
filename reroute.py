import os

from flask import Flask
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp
from routes.user_routes import user_bp
from utils import time_ago
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')

app.jinja_env.filters["time_ago"] = time_ago

app.register_blueprint(auth_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)