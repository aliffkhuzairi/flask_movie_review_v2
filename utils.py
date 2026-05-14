import os, re
from flask import redirect, url_for, session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, date
from uuid import uuid4

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.index"))

        return function(*args, **kwargs)

    return wrapper

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.index"))

        if session.get("user_role") != "admin":
            return redirect(url_for("movie.home"))

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

def get_page(request, default=1):
    page = request.args.get("page", default, type=int)

    if page < 1:
        page = 1

    return page

def build_pagination(total_items, page, per_page):
    total_pages = (total_items + per_page - 1) // per_page

    if total_pages > 0 and page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page

    start_item = offset + 1 if total_items > 0 else 0
    end_item =  min(offset + per_page, total_items)

    pages = []

    if total_pages <= 5:
        pages = list(range(1, total_pages + 1))
    else:
        if page <= 3:
            pages = [1, 2, 3, "...", total_pages]
        elif page >= total_pages - 2:
            pages = [1, "...", total_pages - 2, total_pages - 1, total_pages]
        else:
            pages = [1, "...", page - 1, page, page + 1, "...", total_pages]

    return {
        "page": page,
        "per_page": per_page,
        "offset": offset,
        "total_pages": total_pages,
        "pages": pages,
        "start_item": start_item,
        "end_item": end_item,
    }

def allowed_file(filename, allowed_extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def save_uploaded_file(file, upload_folder, filename_prefix, allowed_extensions):
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename, allowed_extensions):
        return None

    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit(".", 1)[1].lower()

    saved_filename = f"{filename_prefix}_{uuid4().hex}.{ext}"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, saved_filename)
    file.save(file_path)

    return saved_filename


def delete_uploaded_file(upload_folder, filename):
    if not filename:
        return

    file_path = os.path.join(upload_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)

