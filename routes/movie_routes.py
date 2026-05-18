import os
from s3 import upload_to_s3, delete_from_s3
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
from db import db_cursor
from utils import login_required, admin_required, is_valid_rating, get_page, build_pagination, save_uploaded_file, delete_uploaded_file
from uuid import uuid4

movie_bp = Blueprint("movie", __name__)

ALLOWED_SORTS = {"latest", "title", "genre"}
ALLOWED_SORT_DIRS = {"asc", "desc"}
ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}
ALLOWED_POSTER_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

@movie_bp.route("/home")
@login_required
def home():
    with db_cursor() as cur:
        cur.execute("""
            select m.id, m.title, m.genre, m.rel_date, m.poster, m.poster_url, round(avg(r.ratings), 1) as avg_rating
            from movies m
            left join reviews r on m.id = r.mid
            group by m.id, m.title, m.director, m.genre, m.rel_date, m.poster, m.poster_url
            order by m.rel_date desc
            limit 5;
        """)

        movies = cur.fetchall()

        cur.execute("""
            select 
                m.id, 
                m.title, 
                m.rel_date, 
                r.uid, 
                ui.name, 
                ui.avatar, 
                r.review, 
                r.rev_time, 
                r.ratings,
                m.poster,
                m.poster_url
            from reviews r 
            join movies m on r.mid = m.id
            join user_info ui on r.uid = ui.id
            where not exists (
                      select 1 from ties t
                      where t.id = %s and t.opid = r.uid and t.tie = 'mute'
                      )
            order by r.rev_time desc
            limit 6;
        """, (session["user_id"],))

        reviews = cur.fetchall()

        cur.execute("""
            select m.id, m.title, m.genre, m.poster, m.poster_url,
            round(avg(r.ratings), 1) as avg_rating,
            count(r.ratings) as review_count
            from movies m
            join reviews r on m.id = r.mid
            group by m.id, m.title, m.genre, m.poster, m.poster_url
            order by avg_rating desc, review_count desc
            limit 5;
        """)

        top_rated = cur.fetchall()

        cur.execute("""
            select r.uid, ui.name, ui.avatar, count(*) as review_count
            from reviews r
            join user_info ui on r.uid = ui.id
            where not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            )
            group by r.uid, ui.name, ui.avatar
            order by review_count desc
            limit 5;
        """, (session.get("user_id", -1),))

        top_reviewers = cur.fetchall()

    return render_template("home.html",
                           movies=movies,
                           reviews=reviews,
                           top_rated=top_rated,
                           top_reviewers=top_reviewers,
                           user_id=session["user_id"],)

@movie_bp.route("/movies")
@login_required
def movie_list():
    movie_sort = request.args.get("movie_sort", "latest").strip()
    movie_sort_dir = request.args.get("movie_sort_dir", "desc").strip()
    search = request.args.get("search", "").strip()

    if movie_sort not in ALLOWED_SORTS:
        movie_sort = "latest"
    if movie_sort_dir not in ALLOWED_SORT_DIRS:
        movie_sort_dir = "desc"

    sort_columns = {
        "latest": "rel_date",
        "title": "title",
        "genre": "genre"
    }

    order_column = sort_columns[movie_sort]

    search_pattern = f"%{search}%"

    with db_cursor() as cur:
        # COUNT TOTAL MOVIES AFTER SEARCH
        cur.execute("""
            select count(*)
            from movies
            where title ilike %s
            or director ilike %s
            or genre ilike %s;
        """, (search_pattern, search_pattern, search_pattern))

        total_movies = cur.fetchone()[0]

        # MOVIE PAGINATION
        page = get_page(request)
        per_page = 15
        pagination = build_pagination(total_movies, page, per_page)
        page = pagination["page"]
        offset = pagination["offset"]

        # FETCH MOVIE FROM CURENT PAGE
        if movie_sort == "genre":
            cur.execute(f"""
               select m.id, m.title, m.director, m.genre, m.rel_date, m.poster, m.poster_url, round(avg(r.ratings), 1) as avg_rating
               from movies m
               left join reviews r on m.id = r.mid
               where m.title ilike %s
               or m.director ilike %s or m.genre ilike %s
               group by m.id, m.title, m.director, m.genre, m.rel_date, m.poster, m.poster_url
               order by {order_column} {movie_sort_dir}, m.title asc
               limit %s offset %s;
           """, (search_pattern, search_pattern, search_pattern, per_page, offset))

        else:
            cur.execute(f"""
               select m.id, m.title, m.director, m.genre, m.rel_date, m.poster, m.poster_url, round(avg(r.ratings), 1) as avg_rating
               from movies m
               left join reviews r on m.id = r.mid
               where m.title ilike %s
               or m.director ilike %s or m.genre ilike %s
               group by m.id, m.title, m.director, m.genre, m.rel_date, m.poster, m.poster_url
               order by {order_column} {movie_sort_dir}
               limit %s offset %s;
           """,(search_pattern, search_pattern, search_pattern, per_page, offset))

        movies = cur.fetchall()

    return render_template("movies.html",
                           movies=movies,
                           movie_sort=movie_sort,
                           movie_sort_dir=movie_sort_dir,
                           search=search,
                           page=pagination["page"],
                           pages=pagination["pages"],
                           total_pages=pagination["total_pages"],
                           start_movie=pagination["start_item"],
                           end_movie=pagination["end_item"],
                           total_movies=total_movies,
                           user_id=session["user_id"])

@movie_bp.route("/movies/<int:movie_id>", methods=["GET", "POST"])
@login_required
def movie_detail(movie_id):
    if request.method == "POST":
        review = request.form.get("review", "").strip()
        rating = request.form.get("rating", "").strip()

        if not review or not is_valid_rating(rating):
            flash("Please enter a review and a rating from 1-5.", "warning-movie")
            return redirect(url_for("movie.movie_detail", movie_id=movie_id))

        with db_cursor(commit=True) as cur:
            cur.execute("""
                select 1 from reviews
                where mid = %s and uid = %s;
            """,(movie_id, session["user_id"],))

            existing_review = cur.fetchone()

            if existing_review:
                cur.execute("""
                    update reviews
                    set ratings = %s, review = %s, rev_time = now()
                    where mid = %s and uid = %s;
                """,(rating, review, movie_id, session["user_id"]))

                flash("Review updated!", "success-movie")

            else:
                cur.execute("""
                    insert into reviews(mid, uid, ratings, review, rev_time)
                    values(%s, %s, %s, %s, now());
                """,(movie_id, session["user_id"], rating, review))

                flash("Review added!", "success-movie")

        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

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
        cur.execute("""
            select id, title, director, genre, rel_date, poster, poster_url, trailer_url
            from movies
            where id = %s;
        """,(movie_id,))

        movie = cur.fetchone()

        if movie is None:
            return "Movie not found", 404

        # GET TOTAL REVIEWS
        cur.execute("""
            select count(*)
            from reviews r 
            where r.mid = %s
            and not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            );
        """,(movie_id, session["user_id"]))

        total_reviews = cur.fetchone()[0]

        # MOVIE REVIEWS PAGINATION
        page = get_page(request)
        per_page = 5
        pagination = build_pagination(total_reviews, page, per_page)
        page = pagination["page"]
        offset = pagination["offset"]

        # GET PAGINATED REVIEWS
        cur.execute(f"""
            select r.uid, ui.name, ui.avatar, r.review, r.rev_time, r.ratings
            from reviews r 
            join user_info ui on r.uid = ui.id
            where r.mid = %s
            and not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            )
            order by {order_by}
            limit %s offset %s;
        """, (movie_id, session["user_id"], per_page, offset))

        reviews = cur.fetchall()

        cur.execute("""
            select trunc(avg(r.ratings), 2)
            from reviews r
            where r.mid = %s
            and not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            );
        """,(movie_id, session["user_id"],))

        avg_rating = cur.fetchone()[0]

        # GET RATING BREAKDOWN
        cur.execute("""
            select r.ratings, count(*)
            from reviews r
            where r.mid = %s
            and not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            )
            group by r.ratings
            order by r.ratings asc;
        """,(movie_id, session["user_id"],))

        ratings_count_raw = cur.fetchall()

        rating_count_map = {
            int(row[0]): row[1] for row in ratings_count_raw
        }

        rating_breakdown = []

        for rating in range(1, 6):
            count = rating_count_map.get(rating, 0)
            percentage = round((count / total_reviews) * 100) if total_reviews > 0 else 0

            rating_breakdown.append({
                "rating": rating,
                "count": count,
                "percentage": percentage,
            })

        cur.execute("""
            select ratings, review
            from reviews
            where mid = %s and uid = %s;
        """, (movie_id, session["user_id"]))

        user_review = cur.fetchone()

    return render_template("movie.html",
                           movie=movie,
                           reviews=reviews,
                           review_sort=review_sort,
                           page=page,
                           total_reviews=total_reviews,
                           total_pages=pagination["total_pages"],
                           pages=pagination["pages"],
                           start_reviews=pagination["start_item"],
                           end_reviews=pagination["end_item"],
                           avg_rating=avg_rating,
                           rating_breakdown=rating_breakdown,
                           user_review=user_review,
                           user_id=session["user_id"])

def get_poster_upload_folder():
    return os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "posters"
    )


def save_movie_poster(file, movie_id):
    filename = file.filename.lower()
    ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''

    if ext not in ALLOWED_POSTER_EXTENSIONS:
        return None

    content_type_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp'
    }

    content_type = content_type_map.get(ext, 'image/jpeg')
    poster_filename = f"movie_{movie_id}_{uuid4().hex}.{ext}"
    file_data = file.read()

    return upload_to_s3(file_data, poster_filename, 'posters', content_type)


def delete_movie_poster(poster_val):
    if not poster_val:
        return
    if poster_val.startswith('https://'):
        delete_from_s3(poster_val)
    else:
        # Legacy local file
        delete_uploaded_file(
            upload_folder=get_poster_upload_folder(),
            filename=poster_val
        )

@movie_bp.route("/movies/<int:movie_id>/edit", methods=["POST"])
@login_required
@admin_required
def movie_edit(movie_id):
    title = request.form.get("title").strip()
    director = request.form.get("director").strip()
    genre = request.form.get("genre").strip()
    rel_date = request.form.get("rel_date").strip()
    poster_file = request.files.get("poster")
    poster_url = request.form.get("poster_url", "").strip() or None
    trailer_url = request.form.get("trailer_url", "").strip() or None

    old_poster = None
    poster_filename = None

    if not title or not director or not genre or not rel_date:
        flash("All movie fields are required!", "warning-edit")
        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning-edit")
        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                select poster
                from movies
                where id = %s;
            """,(movie_id,))

            old_poster_row = cur.fetchone()

            if old_poster_row is None:
                flash("Movie not found!", "warning-edit")
                return redirect(url_for("movie.movie_list"))

            old_poster = old_poster_row[0]

            poster_filename = old_poster

            if poster_file and poster_file.filename:
                poster_filename = save_movie_poster(poster_file, movie_id)

                if not poster_filename:
                    flash("Poster must be PNG, JPG, JPEG or WEBP", "warning-edit")
                    return redirect(url_for("movie.movie_detail", movie_id=movie_id))

            if poster_filename:

                cur.execute("""
                    update movies
                    set title = %s, director = %s, genre = %s, rel_date = %s, poster = %s, poster_url = %s, trailer_url = %s
                    where id = %s;
                """, (title, director, genre, rel_date, poster_filename, poster_url, trailer_url, movie_id))

            else:
                cur.execute("""
                    update movies
                    set title = %s, director = %s, genre = %s, rel_date = %s, poster_url = %s, trailer_url = %s
                    where id = %s;
                """, (title, director, genre, rel_date, poster_url, trailer_url, movie_id))

                if cur.rowcount == 0:
                    flash("Movie not found!", "error-edit")
                    return redirect(url_for("movie.movie_list"))

        if poster_filename and old_poster:
            delete_movie_poster(old_poster)

        flash("Movie updated!", "success-edit")

    except Exception as err:
        if poster_filename and old_poster:
            delete_movie_poster(old_poster)

        flash(f"Failed to update movie!: {err}", "error-edit")

    return redirect(url_for("movie.movie_detail", movie_id=movie_id))

@movie_bp.route("/movies/<int:movie_id>/delete", methods=["POST"])
@login_required
@admin_required
def movie_delete(movie_id):
    if session.get("user_role") != "admin":
        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

    poster_filename = None

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                select poster
                from movies
                where id = %s;
            """,(movie_id,))

            poster_row = cur.fetchone()

            if poster_row is None:
                flash("Movie not found!", "error-edit")
                return redirect(url_for("movie.movie_list"))

            poster_filename = poster_row[0]

            cur.execute("""
                delete from reviews
                where mid = %s;
            """,(movie_id,))

            cur.execute("""
                delete from movies
                where id = %s;
            """,(movie_id,))

            if cur.rowcount == 0:
                flash("Movie not found!", "error-edit")
                return redirect(url_for("movie.movie_list"))

        if poster_filename:
            delete_movie_poster(poster_filename)

        flash("Movie deleted!", "success-edit")

    except Exception as err:
        flash(f"Failed to delete movie!: {err}", "error-edit")

    return redirect(url_for("movie.movie_list"))


@movie_bp.route("/movies/<int:movie_id>/poster/remove", methods=["POST"])
@login_required
@admin_required
def remove_movie_poster(movie_id):
    poster_filename = None

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                select poster
                from movies
                where id = %s;
            """, (movie_id,))

            poster_row = cur.fetchone()

            if poster_row is None:
                flash("Movie not found!", "error-edit")
                return redirect(url_for("movie.movie_list"))

            poster_filename = poster_row[0]

            if not poster_filename:
                flash("This movie does not have an uploaded poster.", "warning-edit")
                return redirect(url_for("movie.movie_detail", movie_id=movie_id))

            cur.execute("""
                update movies
                set poster = null
                where id = %s;
            """, (movie_id,))

        delete_movie_poster(poster_filename)

        flash("Uploaded poster removed.", "success-edit")

    except Exception as err:
        flash(f"Failed to remove poster!: {err}", "error-edit")

    return redirect(url_for("movie.movie_detail", movie_id=movie_id))