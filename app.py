import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from utils import time_ago
from routes import register_routes
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')

app.jinja_env.filters["time_ago"] = time_ago
app.jinja_env.globals['enumerate'] = enumerate

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)