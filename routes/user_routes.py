from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from utils import login_required, is_valid_email
from db import db_cursor

ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/<user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    current_user_role = session.get("user_role")
    review_sort = request.args.get("review_sort", "latest").strip()

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
            select u.id, u.role, ui.name, ui.email, ui.reg_date
            from users u
            join user_info ui on u.id = ui.id
            where u.id = %s;
        """, (user_id,))

        user_info = cur.fetchone()

        if user_info is None:
            return "User not found", 404

        # REVIEWS PAGINATION
        page = request.args.get("page", 1, type=int)
        per_page = 5
        offset = (page - 1) * per_page

        cur.execute(f"""
            select m.id, m.title, r.ratings, r.review, r.rev_time, m.rel_date
            from reviews r 
            join movies m on r.mid = m.id
            where r.uid = %s
            order by {order_by}
            limit %s offset %s;
        """, (user_id, per_page, offset))

        user_reviews = cur.fetchall()

        cur.execute("""
            select count(*)
            from reviews
            where uid = %s;
        """, (user_id,))

        total_reviews = cur.fetchone()[0]
        total_pages = (total_reviews + per_page - 1) //  per_page

        # ROLE DIFFERENTIATION
        is_self = user_id == session["user_id"]
        is_admin_profile = user_info[1] == "admin"
        is_current_user_admin = current_user_role == "admin"


        # SOCIAL STATUS AND INTERACTIONS
        relationship = None
        followed_users = []
        muted_users = []

        cur.execute("""
                    select ui.id, ui.name
                    from ties t
                    join user_info ui on t.opid = ui.id
                    where t.id = %s and t.tie = 'follow'
                    order by ui.id;
        """, (user_id,))

        followed_users = cur.fetchall()


        if is_self:

            cur.execute("""
                        select ui.id, ui.name
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
                           page=page,
                           review_sort=review_sort,
                           total_pages=total_pages,
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
        return redirect(url_for("user_detail", user_id=user_id))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name and not email:
        flash("Please enter a name or email.", "warning")
        return redirect(url_for("user_detail", user_id=user_id))

    if name and len(name) < 4:
        flash("Name must be at least 4 characters.", "warning")
        return redirect(url_for("user_detail", user_id=user_id))

    if email and not is_valid_email(email):
        flash("Please enter a valid email address.", "warning")
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

    flash("Your profile has been updated.", "success")
    return redirect(url_for("user.user_detail", user_id=user_id))

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
        return redirect(url_for("user_detail", user_id=target_user_id))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            insert into ties(id, opid, tie)
            values(%s, %s, 'follow')
            on conflict (id, opid) do update
            set tie = 'follow';
        """,(session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=target_user_id))

@user_bp.route("/unfollow/<target_user_id>", methods=["POST"])
@login_required
def unfollow_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from ties
            where id = %s and opid = %s and tie = 'follow';
        """, (session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=session["user_id"]))

@user_bp.route("/mute/<target_user_id>", methods=["POST"])
@login_required
def mute_user(target_user_id):
    if not can_manage_relationship(target_user_id):
        return redirect(url_for("user_detail", user_id=target_user_id))

    with db_cursor(commit=True) as cur:
        cur.execute("""
            insert into ties(id, opid, tie)
            values (%s, %s, 'mute') 
            on conflict (id, opid) do update
            set tie = 'mute';
        """, (session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=session["user_id"]))

@user_bp.route("/unmute/<target_user_id>", methods=["POST"])
@login_required
def unmute_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete
            from ties
            where id = %s and opid = %s and tie = 'mute';
                    """, (session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=target_user_id))

@user_bp.route("/add-movie", methods=["POST"])
@login_required
def add_movie():
    title =request.form.get("movie_title", "").strip()
    director = request.form.get("director", "").strip()
    genre = request.form.get("genre", "").strip()
    rel_date = request.form.get("rel_date", "").strip()

    if not title or not director or not genre or not rel_date:
        flash("All fields are required.", "warning")
        return redirect(url_for("user.user_detail", user_id=session["user_id"]))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning")
        return redirect(url_for("user.user_detail", user_id=session["user_id"]))

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                insert into movies(title, director, genre, rel_date)
                values(%s, %s, %s, %s)
                on conflict (title, director, genre, rel_date) do nothing;
            """, (title, director, genre, rel_date))

            if cur.rowcount == 0:
                flash("Movie already exists.", "warning")
            else:
                flash("Movie added successfully.", "success")

    except Exception as err:
        flash(f"Failed to add movie: {err}", "error")

    return redirect(url_for("user.user_detail", user_id=session["user_id"]))

@user_bp.route("/review/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_review(movie_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from reviews
            where mid = %s and uid = %s;
        """,(movie_id, session["user_id"]))

    flash("Review deleted.", "success")
    return redirect(url_for("user_detail", user_id=session["user_id"]))