import re
from flask import redirect, url_for, session
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime, date

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("index"))

        return function(*args, **kwargs)

    return wrapper

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("index"))

        if session.get("user_role") != "admin":
            return redirect(url_for("home"))

        return function(*args, **kwargs)

    return wrapper

def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

def is_valid_rating(rating):
    return rating.isdigit() and 0 <= int(rating) <= 5

def password_matches(stored_password, submitted_password):
    if stored_password.startswith(("pbkdf2:", "scrypt:")):
        return check_password_hash(stored_password, submitted_password)
    return stored_password == submitted_password

def time_ago(value):
    if value is None:
        return ""

    if isinstance(value, date) and not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())

    now = datetime.now()
    diff = now - value

    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    weeks = days // 7
    months = days // 30
    years = days // 365

    if seconds < 60:
        return "just now"
    elif minutes < 60:
        return f"{minutes}m"
    elif hours < 24:
        return f"{hours}h"
    elif days == 1:
        return "Yesterday"
    elif days < 7:
        return f"{days}d"
    elif weeks == 1:
        return "Last week"
    elif weeks < 5:
        return f"{weeks}w"
    elif months < 12:
        return f"{months}mo"
    else:
        return f"{years}y"

