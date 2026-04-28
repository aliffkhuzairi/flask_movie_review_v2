from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash

from db import db_cursor
from utils import password_matches

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("login.html")

@auth_bp.route("/auth", methods=["POST"])
def auth():
    user_id = request.form.get("user_id", "").strip()
    password = request.form.get("password", "").strip()

    if not user_id or not password:
        flash("Please enter both ID and password", "warning")
        return redirect(url_for("index"))

    with db_cursor() as cur:
        cur.execute("""
            select id, password, role
            from users
            where id = %s;
        """, (user_id,))

        user = cur.fetchone()

    if user and password_matches(user[1], password):
        session.clear()
        session["user_id"] = user[0]
        session["user_role"] = user[2]
        return redirect(url_for("movie.home"))

    flash("ID or password are invalid.", "error")
    return redirect(url_for("index"))

@auth_bp.route("/signup")
def signup_page():
    return render_template("signup.html")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    user_id = request.form.get("user_id", "").strip()
    password = request.form.get("password", "").strip()

    if not user_id or not password:
        flash("Please enter both ID and password", "warning")
        return redirect(url_for("signup_page"))

    if len(password) < 8:
        flash("Password must be at least 8 characters", "warning")
        return redirect(url_for("signup_page"))

    hashed_password = generate_password_hash(password)

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                insert into users(id, password, role)
                values(%s, %s, 'user');
            """, (user_id, hashed_password))

            cur.execute("""
                insert into user_info(id, reg_date)
                values(%s, now());
            """,(user_id,))

        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for("index"))

    except Exception:
        flash("Sign up failed, ID may already exist.", "error")
        return redirect(url_for("signup_page"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))