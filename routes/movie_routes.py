from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from db import db_cursor
from utils import login_required, is_valid_rating

movie_bp = Blueprint("movie", __name__)

ALLOWED_SORTS = {"latest", "title", "genre"}
ALLOWED_SORT_DIRS = {"asc", "desc"}
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
        if movie_sort == "genre":
            cur.execute(f"""
                select id, title, director, genre, rel_date
                from movies
                where title ilike %s
                or director ilike %s or genre ilike %s
                order by {order_column} {movie_sort_dir}, title asc;
            """, (search_pattern, search_pattern, search_pattern))

        else:
            cur.execute(f"""
                select id, title, director, genre, rel_date
                from movies
                where title ilike %s
                or director ilike %s or genre ilike %s
                order by {order_column} {movie_sort_dir};
            """,(search_pattern, search_pattern, search_pattern))

        movies = cur.fetchall()

    return render_template("movies.html",
                           movies=movies,
                           movie_sort=movie_sort,
                           movie_sort_dir=movie_sort_dir,
                           search=search,
                           user_id=session["user_id"])

@movie_bp.route("/movies/<int:movie_id>", methods=["GET", "POST"])
@login_required
def movie_detail(movie_id):
    if request.method == "POST":
        review = request.form.get("review", "").strip()
        rating = request.form.get("rating", "").strip()

        if not review or not is_valid_rating(rating):
            flash("Please enter a review and a rating from 0-5.")
            return redirect(url_for("movie_detail", movie_id=movie_id))

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

    with db_cursor() as cur:
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
            where id = %s;
        """,(movie_id,))

        movie = cur.fetchone()

        if movie is None:
            return "Movie not found", 404

        cur.execute("""
            select r.uid, r.review, r.rev_time, r.ratings
            from reviews r 
            where r.mid = %s
            and not exists (
                select 1 from ties t
                where t.id = %s and t.opid = r.uid and t.tie = 'mute'
            )
            order by r.rev_time desc;
        """, (movie_id, session["user_id"],))

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
                           avg_rating=avg_rating,
                           user_review=user_review,
                           user_id=session["user_id"])