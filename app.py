import psycopg2, os, re
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from contextlib import contextmanager
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')

ALLOWED_SORTS = {"latest", "title", "genre"}
ALLOWED_SORT_DIRS = {"asc", "desc"}
ALLOWED_GENRES = {"action", "comedy", "drama", "fantasy", "romance", "thriller", "western"}

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DATABASE_NAME', 'term_project'),
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', '@100pluS'),
        host=os.getenv('DATABASE_HOST', 'localhost'),
        port=os.getenv('DATABASE_PORT', '5432'),
    )

@contextmanager
def db_cursor(commit=False):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        yield cur
        if commit:
            conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

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

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
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
        return redirect(url_for("home"))

    flash("ID or password are invalid.", "error")
    return redirect(url_for("index"))

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
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
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/home")
@login_required
def home():
    with db_cursor() as cur:
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
            order by rel_date desc
            limit 4;
        """)

        movies = cur.fetchall()

        cur.execute("""
            select r.ratings, r.uid, m.title, r.review, r.rev_time, m.genre
            from reviews r 
            join movies m on r.mid = m.id
            where not exists (
                      select 1 from ties t
                      where t.id = %s and t.opid = r.uid and t.tie = 'mute'
                      )
            order by r.rev_time desc
            limit 5;
        """, (session["user_id"],))

        reviews = cur.fetchall()

    return render_template("home.html",
                           movies=movies,
                           reviews=reviews,
                           user_id=session["user_id"],)

@app.route("/movies")
@login_required
def movie_list():
    movie_sort = request.args.get("movie_sort", "latest").strip()
    movie_sort_dir = request.args.get("movie_sort_dir", "desc").strip()

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

    with db_cursor() as cur:
        if movie_sort == "genre":
            cur.execute(f"""
                select id, title, director, genre, rel_date
                from movies
                order by {order_column} {movie_sort_dir}, title asc;
            """)

        else:
            cur.execute(f"""
                select id, title, director, genre, rel_date
                from movies
                order by {order_column} {movie_sort_dir};
            """)

        movies = cur.fetchall()

    return render_template("movies.html",
                           movies=movies,
                           movie_sort=movie_sort,
                           movie_sort_dir=movie_sort_dir,
                           user_id=session["user_id"])

@app.route("/movies/<int:movie_id>", methods=["GET", "POST"])
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

        return redirect(url_for("movie_detail", movie_id=movie_id))

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
            select r.ratings, r.uid, r.review, r.rev_time
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

@app.route("/user/<user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    current_user_role = session.get("user_role")

    with db_cursor() as cur:
        cur.execute("""
            select u.id, u.role, ui.name, ui.email, ui.reg_date
            from users u
            join user_info ui on u.id = ui.id
            where u.id = %s;
        """, (user_id,))

        user_info = cur.fetchone()

        if user_info is None:
            return "User not found", 404

        cur.execute("""
            select m.id, m.title, r.ratings, r.review, r.rev_time, m.genre
            from reviews r 
            join movies m on r.mid = m.id
            where r.uid = %s
            order by r.rev_time desc;
        """, (user_id,))
        user_reviews = cur.fetchall()

        is_self = user_id == session["user_id"]
        is_admin_profile = user_info[1] == "admin"
        is_current_user_admin = current_user_role == "admin"

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
                           is_self=is_self,
                           is_admin_profile=is_admin_profile,
                           is_current_user_admin=is_current_user_admin,
                           relationship=relationship,
                           followed_users=followed_users,
                           muted_users=muted_users,
                           followed_count=followed_count,
                           muted_count=muted_count,
                           clear_form=clear_form)

@app.route("/user/<user_id>/edit", methods=["POST"])
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
    return redirect(url_for("user_detail", user_id=user_id))

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

@app.route("/follow/<target_user_id>", methods=["POST"])
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

@app.route("/unfollow/<target_user_id>", methods=["POST"])
@login_required
def unfollow_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from ties
            where id = %s and opid = %s and tie = 'follow';
        """, (session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=session["user_id"]))

@app.route("/mute/<target_user_id>", methods=["POST"])
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

@app.route("/unmute/<target_user_id>", methods=["POST"])
@login_required
def unmute_user(target_user_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete
            from ties
            where id = %s and opid = %s and tie = 'mute';
                    """, (session["user_id"], target_user_id))

    return redirect(url_for("user_detail", user_id=target_user_id))

@app.route("/add-movie", methods=["POST"])
@login_required
def add_movie():
    title =request.form.get("movie_title", "").strip()
    director = request.form.get("director", "").strip()
    genre = request.form.get("genre", "").strip()
    rel_date = request.form.get("rel_date", "").strip()

    if not title or not director or not genre or not rel_date:
        flash("All fields are required.", "warning")
        return redirect(url_for("user_detail", user_id=session["user_id"]))

    if genre not in ALLOWED_GENRES:
        flash("Please select a valid genre.", "warning")
        return redirect(url_for("user_detail", user_id=session["user_id"]))

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

    return redirect(url_for("user_detail", user_id=session["user_id"]))

@app.route("/review/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_review(movie_id):
    with db_cursor(commit=True) as cur:
        cur.execute("""
            delete from reviews
            where mid = %s and uid = %s;
        """,(movie_id, session["user_id"]))

    flash("Review deleted.", "success")
    return redirect(url_for("user_detail", user_id=session["user_id"]))

if __name__ == "__main__":
    app.run(debug=True)