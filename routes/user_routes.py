import os, base64
from flask import render_template, request, redirect, url_for, flash, session, Blueprint, current_app
from utils import login_required, is_valid_email, get_page, build_pagination
from db import db_cursor
from werkzeug.utils import secure_filename
from uuid import uuid4

ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}
ALLOWED_TABS = {"overview", "reviews", "connections", "settings"}
ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

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

        # USER REVIEWS PAGINATION
        page = get_page(request)
        per_page = 5
        pagination = build_pagination(total_reviews, page, per_page)
        page = pagination["page"]
        offset = pagination["offset"]

        # FETCH PAGINATED REVIEWS
        cur.execute(f"""
            select m.id, m.title, r.ratings, r.review, r.rev_time, m.rel_date
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
        return redirect(url_for("user_detail", user_id=user_id))

    if name and len(name) < 4:
        flash("Name must be at least 4 characters.", "warning-profile")
        return redirect(url_for("user_detail", user_id=user_id))

    if email and not is_valid_email(email):
        flash("Please enter a valid email address.", "warning-profile")
        return redirect(url_for("user_detail", user_id=user_id))

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
    return redirect(url_for("user.user_detail", user_id=user_id))

@user_bp.route("/user/<user_id>/avatar", methods=["POST"])
@login_required
def update_avatar(user_id):
    if session["user_id"] != user_id:
        return redirect(url_for("user.user_detail", user_id=user_id))

    cropped_avatar = request.form.get("cropped_avatar", "").strip()

    if not cropped_avatar:
        flash("Please crop and save an avatar before updating.", "warning-avatar")
        return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

    try:
        header, encoded = cropped_avatar.split(",", 1)

        if "image/jpeg" in header:
            ext = "jpg"
        elif "image/png" in header:
            ext = "png"
        elif "image/webp" in header:
            ext = "webp"
        else:
            flash("Avatar must be a PNG, JPG, JPEG, or WEBP image.", "warning-avatar")
            return redirect(url_for("user.user_detail", user_id=user_id, tab="settings"))

        avatar_data = base64.b64decode(encoded)
        avatar_filename = f"{user_id}_{uuid4().hex}.{ext}"

        upload_folder = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            "avatars"
        )

        os.makedirs(upload_folder, exist_ok=True)

        avatar_path = os.path.join(upload_folder, avatar_filename)

        with open(avatar_path, "wb") as avatar_file:
            avatar_file.write(avatar_data)

        with db_cursor(commit=True) as cur:
            cur.execute("""
                update user_info
                set avatar = %s
                where id = %s;
            """, (avatar_filename, user_id))

    except Exception:
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
        avatar_filename = avatar_row[0] if avatar_row else None

        cur.execute("""
                    update user_info
                    set avatar = null
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

    return redirect(url_for("user.user_detail", user_id=session["user_id"]))

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

    return redirect(url_for("user.user_detail", user_id=session["user_id"]))

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
def add_movie():
    title =request.form.get("movie_title", "").strip()
    director = request.form.get("director", "").strip()
    genre = request.form.get("genre", "").strip()
    rel_date = request.form.get("rel_date", "").strip()

    if not title or not director or not genre or not rel_date:
        flash("All fields are required.", "warning-admin")
        return redirect(url_for("user.user_detail", user_id=session["user_id"]))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning-admin")
        return redirect(url_for("user.user_detail", user_id=session["user_id"]))

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                insert into movies(title, director, genre, rel_date)
                values(%s, %s, %s, %s)
                on conflict (title, rel_date) do nothing;
            """, (title, director, genre, rel_date))

            if cur.rowcount == 0:
                flash("Movie already exists!", "warning-admin")
            else:
                flash("Movie added successfully!", "success-admin")

    except Exception as err:
        flash(f"Failed to add movie!: {err}", "error-admin")

    return redirect(url_for("user.user_detail", user_id=session["user_id"]))

@user_bp.route("/review/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_review(movie_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from reviews
            where mid = %s and uid = %s;
        """,(movie_id, session["user_id"]))

    flash("Review deleted!", "success-delete")
    return redirect(url_for("user.user_detail", user_id=session["user_id"]))