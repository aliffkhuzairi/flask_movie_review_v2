from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from db import db_cursor
from utils import login_required, admin_required, is_valid_rating, get_page, build_pagination

movie_bp = Blueprint("movie", __name__)

ALLOWED_SORTS = {"latest", "title", "genre"}
ALLOWED_SORT_DIRS = {"asc", "desc"}
ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}

@movie_bp.route("/home")
@login_required
def home():
    with db_cursor() as cur:
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
            order by rel_date desc
            limit 5;
        """)

        movies = cur.fetchall()

        cur.execute("""
            select m.id, m.title, m.rel_date, r.uid, r.review, r.rev_time, r.ratings 
            from reviews r 
            join movies m on r.mid = m.id
            where not exists (
                      select 1 from ties t
                      where t.id = %s and t.opid = r.uid and t.tie = 'mute'
                      )
            order by r.rev_time desc
            limit 6;
        """, (session["user_id"],))

        reviews = cur.fetchall()

    return render_template("home.html",
                           movies=movies,
                           reviews=reviews,
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
               select id, title, director, genre, rel_date
               from movies
               where title ilike %s
               or director ilike %s or genre ilike %s
               order by {order_column} {movie_sort_dir}, title asc
               limit %s offset %s;
           """, (search_pattern, search_pattern, search_pattern, per_page, offset))

        else:
            cur.execute(f"""
               select id, title, director, genre, rel_date
               from movies
               where title ilike %s
               or director ilike %s or genre ilike %s
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
            flash("Please enter a review and a rating from 0-5.")
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

                flash("Review updated!", "success")

            else:
                cur.execute("""
                    insert into reviews(mid, uid, ratings, review, rev_time)
                    values(%s, %s, %s, %s, now());
                """,(movie_id, session["user_id"], rating, review))

                flash("Review added!", "success")

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
            select id, title, director, genre, rel_date
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
            select r.uid, r.review, r.rev_time, r.ratings
            from reviews r 
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
                           user_review=user_review,
                           user_id=session["user_id"])

@movie_bp.route("/movies/<int:movie_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def movie_edit(movie_id):
    title = request.form.get("title").strip()
    director = request.form.get("director").strip()
    genre = request.form.get("genre").strip()
    rel_date = request.form.get("rel_date").strip()

    if not title or not director or not genre or not rel_date:
        flash("All movie fields are required!", "warning-movie")
        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning-movie")
        return redirect(url_for("movie.movie_detail", movie_id=movie_id))

    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                update movies
                set title = %s, director = %s, genre = %s, rel_date = %s
                where id = %s;
            """, (title, director, genre, rel_date, movie_id))

            if cur.rowcount == 0:
                flash("Movie not found!", "error-movie")
            else:
                flash("Movie successfully updated!", "success-movie")

    except Exception as err:
        flash(f"Failed to update movie!: {err}", "error-movie")

    return redirect(url_for("movie.movie_detail", movie_id=movie_id))