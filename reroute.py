import os

from flask import Flask
from routes.auth_routes import auth_bp
from utils import time_ago
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')

ALLOWED_SORTS = {"latest", "title", "genre"}
ALLOWED_SORT_DIRS = {"asc", "desc"}
ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}

app.jinja_env.filters["time_ago"] = time_ago

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)