import os, base64
from flask import render_template, request, redirect, url_for, flash, session, Blueprint, current_app
from s3 import upload_to_s3, delete_from_s3

from routes.movie_routes import save_movie_poster, delete_movie_poster
from utils import login_required, is_valid_email, get_page, build_pagination, admin_required
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_cursor
from uuid import uuid4

ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}
ALLOWED_TABS = {"overview", "reviews", "connections", "settings", "admin-panel"}
ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_avatar(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_AVATAR_EXTENSIONS

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/<user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    current_user_role = session.get("user_role")
    review_sort = request.args.get("review_sort", "latest").strip()
    active_tab = request.args.get("tab", "overview").strip()

    if active_tab not in ALLOWED_TABS:
        active_tab = "overview"

    sort_review = ["latest", "highest", "lowest"]

    if review_sort not in sort_review:
        review_sort = "latest"

    # REVIEW SORT SQL COMMAND
    if review_sort == "highest":
        order_by = "r.ratings desc, r.rev_time desc"
    elif review_sort == "lowest":
        order_by = "r.ratings asc, r.rev_time desc"
    else:
        order_by = "r.rev_time desc"

    with db_cursor() as cur:

        # GET USER INFO
        cur.execute("""
            select u.id, u.role, ui.name, ui.email, ui.reg_date, ui.avatar
            from users u
            join user_info ui on u.id = ui.id
            where u.id = %s;
        """, (user_id,))

        user_info = cur.fetchone()

        if user_info is None:
            return "User not found", 404

        # GET TOTAL REVIEWS
        cur.execute("""
            select count(*)
            from reviews
            where uid = %s;
        """,(user_id,))

        total_reviews = cur.fetchone()[0]

        # GET USER REVIEW STATS
        cur.execute("""
            select trunc(avg(r.ratings), 2)
            from reviews r
            where r.uid = %s;
        """,(user_id,))

        avg_rating_given = cur.fetchone()[0]

        cur.execute("""
            select m.genre, count(*) as genre_count
            from reviews r
            join movies m on r.mid = m.id
            where r.uid = %s group by m.genre
            order by genre_count desc, m.genre asc
            limit 1;
        """,(user_id,))

        top_genre_row = cur.fetchone()
        top_genre = top_genre_row[0] if top_genre_row else None

        cur.execute("""
            select max(r.rev_time)
            from reviews r
            where r.uid = %s;
        """,(user_id,))

        latest_review_date = cur.fetchone()[0]

        cur.execute("""
            select m.id, m.title, m.poster, m.poster_url, m.rel_date
            from reviews r
            join movies m on r.mid = m.id
            where r.uid = %s
            order by r.rev_time desc
            limit 4;
        """, (user_id,))
        recent_watches = cur.fetchall()

        # USER REVIEWS PAGINATION
        page = get_page(request)
        per_page = 6
        pagination = build_pagination(total_reviews, page, per_page)
        page = pagination["page"]
        offset = pagination["offset"]

        # FETCH PAGINATED REVIEWS
        cur.execute(f"""
            select m.id, m.title, r.ratings, r.review, r.rev_time, m.rel_date,
                   m.poster, m.poster_url
            from reviews r
            join movies m on r.mid = m.id
            where uid = %s
            order by {order_by}
            limit %s offset %s;
        """,(user_id, per_page, offset))

        user_reviews = cur.fetchall()

        # ROLE DIFFERENTIATION
        is_self = user_id == session["user_id"]
        is_admin_profile = user_info[1] == "admin"
        is_current_user_admin = current_user_role == "admin"

        if not is_self:
            active_tab = "reviews"

        if is_self and is_current_user_admin and active_tab == "connections":
            active_tab = "overview"

        # SOCIAL STATUS AND INTERACTIONS
        relationship = None
        followed_users = []
        muted_users = []

        cur.execute("""
                    select ui.id, ui.name, ui.avatar
                    from ties t
                    join user_info ui on t.opid = ui.id
                    where t.id = %s and t.tie = 'follow'
                    order by ui.id;
        """, (user_id,))

        followed_users = cur.fetchall()

        if is_self:

            cur.execute("""
                        select ui.id, ui.name, ui.avatar
                        from ties t
                        join user_info ui on t.opid = ui.id
                        where t.id = %s and t.tie = 'mute'
                        order by ui.id;
                        """, (user_id,))

            muted_users = cur.fetchall()

        elif not is_admin_profile and not is_current_user_admin:
            cur.execute("""
                select tie from ties
                where id = %s and opid = %s;
            """,(session["user_id"], user_id,))

            relation_row = cur.fetchone()

            if relation_row:
                relationship = relation_row[0]

    followed_count = len(followed_users)
    muted_count = len(muted_users)
    clear_form = session.pop("clear_form", False)

    return render_template("user_info.html",
                           user_info=user_info,
                           user_reviews=user_reviews,
                           user_id=session["user_id"],
                           review_sort=review_sort,
                           active_tab=active_tab,
                           total_reviews=total_reviews,
                           avg_rating_given=avg_rating_given,
                           top_genre=top_genre,
                           latest_review_date=latest_review_date,
                           recent_watches=recent_watches,
                           pages=pagination["pages"],
                           page=pagination["page"],
                           total_pages=pagination["total_pages"],
                           start_reviews=pagination["start_item"],
                           end_reviews=pagination["end_item"],
                           is_self=is_self,
                           is_admin_profile=is_admin_profile,
                           is_current_user_admin=is_current_user_admin,
                           relationship=relationship,
                           followed_users=followed_users,
                           muted_users=muted_users,
                           followed_count=followed_count,
                           muted_count=muted_count,
                           clear_form=clear_form)

@user_bp.route("/user/<user_id>/edit", methods=["POST"])
@login_required
def edit_user_profile(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name and not email:
        flash("Please enter a name or email.", "warning-profile")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    if name and len(name) < 4:
        flash("Name must be at least 4 characters.", "warning-profile")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    if email and not is_valid_email(email):
        flash("Please enter a valid email address.", "warning-profile")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    with db_cursor(commit=True) as cur:
        if name:
            cur.execute("""
                update user_info
                set name = %s
                where id = %s;
            """, (name, user_id))

        if email:
            cur.execute("""
                update user_info
                set email = %s
                where id = %s;
            """, (email, user_id))

    flash("Your profile has been updated.", "success-profile")
    return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

@user_bp.route("/user/<user_id>/password", methods=["POST"])
@login_required
def change_password(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    current_password = request.form.get("current-password", "").strip()
    new_password = request.form.get("new-password", "").strip()
    confirm_password = request.form.get("confirm-password", "").strip()

    if not current_password or not new_password or not confirm_password:
        flash("All fields are required.", "warning-password")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    if len(new_password) < 8:
        flash("Password must be at least 8 characters.", "warning-password")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "warning-password")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            select password
            from users
            where id = %s;
        """, (user_id,))

        user = cur.fetchone()

        if user is None:
            flash("User does not exist.", "error-password")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        stored_password = user[0]

        if not check_password_hash(stored_password, current_password):
            flash("Current password does not match.", "warning-password")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        if check_password_hash(stored_password, new_password):
            flash("New password cannot be the same as your current password.", "warning-password")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        hashed_password = generate_password_hash(new_password)

        cur.execute("""
            update users
            set password = %s
            where id = %s;
        """, (hashed_password, user_id))

    flash("Password has been changed.", "success-password")
    return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

@user_bp.route("/user/<user_id>/avatar", methods=["POST"])
@login_required
def update_avatar(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    cropped_avatar = request.form.get("cropped_avatar", "").strip()

    if not cropped_avatar:
        flash("Please crop and save an avatar before updating.", "warning-avatar")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    ext = "jpg"
    content_type = "image/jpeg"

    try:
        header, encoded = cropped_avatar.split(",", 1)

        if "image/jpeg" in header:
            ext = "jpg"
            content_type = "image/jpeg"
        elif "image/png" in header:
            ext = "png"
            content_type = "image/png"
        elif "image/webp" in header:
            ext = "webp"
            content_type = "image/webp"
        else:
            flash("Avatar must be a PNG, JPG, JPEG, or WEBP image.", "warning-avatar")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        avatar_data = base64.b64decode(encoded)
        avatar_filename = f"{user_id}_{uuid4().hex}.{ext}"

        with db_cursor() as cur:
            cur.execute("SELECT avatar FROM user_info WHERE id = %s", (user_id,))
            old = cur.fetchone()
            if old and old[0] and old[0].startswith('https://'):
                delete_from_s3(old[0])

        avatar_url = upload_to_s3(avatar_data, avatar_filename, 'avatars', content_type)

        with db_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE user_info SET avatar = %s WHERE id = %s;
            """, (avatar_url, user_id))

    except Exception as e:
        flash("Failed to update avatar.", "error-avatar")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    flash("Avatar updated.", "success-avatar")
    return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

@user_bp.route("/user/<user_id>/avatar/remove", methods=["POST"])
@login_required
def remove_avatar(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    with db_cursor(commit=True) as cur:
        cur.execute("""
                    select avatar
                    from user_info
                    where id = %s;
                    """, (user_id,))

        avatar_row = cur.fetchone()
        avatar_val = avatar_row[0] if avatar_row else None

        cur.execute("""
                    update user_info
                    set avatar = null
                    where id = %s;
                    """, (user_id,))

    if avatar_val:
        if avatar_val.startswith('https://'):
            delete_from_s3(avatar_val)
        else:
            # Legacy local file
            avatar_path = os.path.join(
                current_app.root_path, "static", "uploads", "avatars", avatar_val
            )
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

    flash("Profile photo removed.", "success-avatar")
    return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

def can_manage_relationship(target_user_id):
    if session.get("user_role") == "admin":
        return False

    if session["user_id"] == target_user_id:
        return False

    with db_cursor() as cur:
        cur.execute("""
            select role from users
            where id = %s;
        """, (target_user_id,))
        target_user = cur.fetchone()

    if target_user is None or target_user[0] == "admin":
        return False

    return True

@user_bp.route("/follow/<target_user_id>", methods=["POST"])
@login_required
def follow_user(target_user_id):

    if not can_manage_relationship(target_user_id):
        return redirect(url_for("user.user_detail", user_id=target_user_id))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            insert into ties(id, opid, tie)
            values(%s, %s, 'follow')
            on conflict (id, opid) do update
            set tie = 'follow';
        """,(session["user_id"], target_user_id))

    return redirect(url_for("user.user_detail", user_id=target_user_id))

@user_bp.route("/unfollow/<target_user_id>", methods=["POST"])
@login_required
def unfollow_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from ties
            where id = %s and opid = %s and tie = 'follow';
        """, (session["user_id"], target_user_id))

    return redirect(url_for("user.user_detail", user_id=target_user_id))

@user_bp.route("/mute/<target_user_id>", methods=["POST"])
@login_required
def mute_user(target_user_id):
    if not can_manage_relationship(target_user_id):
        return redirect(url_for("user.user_detail", user_id=target_user_id))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            insert into ties(id, opid, tie)
            values (%s, %s, 'mute') 
            on conflict (id, opid) do update
            set tie = 'mute';
        """, (session["user_id"], target_user_id))

    return redirect(url_for("user.user_detail", user_id=target_user_id))

@user_bp.route("/unmute/<target_user_id>", methods=["POST"])
@login_required
def unmute_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete
            from ties
            where id = %s and opid = %s and tie = 'mute';
                    """, (session["user_id"], target_user_id))

    return redirect(url_for("user.user_detail", user_id=target_user_id))

@user_bp.route("/add-movie", methods=["POST"])
@login_required
@admin_required
def add_movie():
    title =request.form.get("movie_title", "").strip()
    director = request.form.get("director", "").strip()
    genre = request.form.get("genre", "").strip()
    rel_date = request.form.get("rel_date", "").strip()
    poster_file = request.files.get("poster")
    poster_url = request.form.get("poster_url", "").strip() or None
    trailer_url = request.form.get("trailer_url", "").strip() or None

    poster_filename = None

    if not title or not director or not genre or not rel_date:
        flash("All fields are required.", "warning-admin")
        return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="admin-panel"))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning-admin")
        return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="admin-panel"))

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                insert into movies(title, director, genre, rel_date, poster_url, trailer_url)
                values(%s, %s, %s, %s, %s, %s)
                on conflict (title, rel_date) do nothing
                returning id;
            """, (title, director, genre, rel_date, poster_url, trailer_url))

            movie_row = cur.fetchone()

            if movie_row is None:
                flash("Movie already exists.", "warning-admin")
                return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="admin-panel"))

            movie_id = movie_row[0]

            if poster_file and poster_file.filename:
                poster_filename = save_movie_poster(poster_file, movie_id)

                if not poster_filename:
                    flash("Poster must be PNG, JPG, JPEG, or WEBP", "warning-admin")
                    return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="admin-panel"))

                cur.execute("""
                    update movies
                    set poster = %s
                    where id = %s
                """,(poster_filename, movie_id))

        flash("Movie added successfully!", "success-admin")

    except Exception as err:
        if poster_filename:
            delete_movie_poster(poster_filename)

        flash(f"Failed to add movie!: {err}", "error-admin")

    return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="admin-panel"))

@user_bp.route("/review/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_review(movie_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from reviews
            where mid = %s and uid = %s;
        """,(movie_id, session["user_id"]))

    flash("Review deleted!", "success-delete")
    return redirect(url_for("user.user_detail", user_id=session["user_id"], tab="reviews"))

@user_bp.route("/user/<user_id>/delete", methods=["POST"])
@login_required
def delete_account(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    if session.get("user_role") == "admin":
        flash("Admin accounts cannot be deleted from this page.", "warning-delete-account")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    confirm_text = request.form.get("confirm_delete", "").strip()
    password = request.form.get("delete_password", "").strip()

    if confirm_text != "DELETE":
        flash("Type DELETE to confirm account deletion.", "warning-delete-account")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    if not password:
        flash("Please enter your password to delete your account.", "warning-delete-account")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            select u.password, ui.avatar
            from users u
            join user_info ui on u.id = ui.id
            where u.id = %s;
        """, (user_id,))

        user = cur.fetchone()

        if user is None:
            flash("User does not exist.", "error-delete-account")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        stored_password = user[0]
        avatar_filename = user[1]

        if not check_password_hash(stored_password, password):
            flash("Password is incorrect.", "error-delete-account")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        cur.execute("""
            delete from ties
            where id = %s or opid = %s;
        """, (user_id, user_id))

        cur.execute("""
            delete from reviews
            where uid = %s;
        """, (user_id,))

        cur.execute("""
            delete from user_info
            where id = %s;
        """, (user_id,))

        cur.execute("""
            delete from users
            where id = %s;
        """, (user_id,))

    if avatar_filename:
        avatar_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            "avatars",
            avatar_filename
        )

        if os.path.exists(avatar_path):
            os.remove(avatar_path)

    session.clear()
    flash("Your account has been deleted.", "success")
    return redirect(url_for("auth.index"))